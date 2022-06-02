#!/usr/bin/env python3
"""
read the config yaml file
"""

#################################
# for handling relative imports #
#################################
if __name__ == '__main__':
    import sys
    from pathlib import Path
    current_file = Path(__file__).resolve()
    root = next(elem for elem in current_file.parents
                if str(elem).endswith('src'))
    sys.path.append(str(root))
    # remove the current file's directory from sys.path
    try:
        sys.path.remove(str(current_file.parent))
    except ValueError:  # Already removed
        pass
#################################

import yaml
import argparse

from sys import argv
from loguru import logger
from os.path import join

from classes.project import Project
from classes.bloomberg import BloombergData
from classes.additional import Additional
from classes.window import Window
from classes.project import Project
from classes.operation import Operation
from classes.predict import Predict
from classes.sector import Sector
from clean.dataclean import CleanData

from utils.error_handling import HandleErrors
from utils.utils import relative_file_path
from utils.enums import OptimizerType, ModelType, SectorType
from utils.model_type_map import model_type_map
from predict.optimization_map import optimizer_type_map
from typing import Any, List, Optional, Dict

from constants import config_folder


def read_config(args: Any) -> List[Project]:
    """
    read a config file
    """
    # read in the config data from the passed in file path
    config_file_path = relative_file_path(args.config)
    config_data: Optional[Dict[Any]] = None
    with open(config_file_path, 'r') as config_file:
        config_data = yaml.safe_load(config_file)

    # TODO - pre-process config file
    # static_validate_config(config_data)

    # keys
    sectors_key: str = 'sectors'
    input_key: str = 'data'

    window_key = 'window'
    predict_key = 'predict'
    bloomberg_data_key = 'bloomberg'
    lag_key = 'lag'

    additional_data_key = 'additional'

    operations_key = 'operations'
    operations_output_columns_key = 'output_columns'
    operation_type_key = 'operation'
    operations_input_columns_key = 'input_columns'
    operations_arguments_key = 'arguments'
    operations_remove_key = 'remove'

    models_key = 'models'
    type_key = 'type'

    optimization_key = 'optimize'
    benchmark_key = 'benchmark'
    black_litterman_key = 'black_litterman'
    hrp_key = 'hrp'
    predictions_key = 'predictions'

    rebalance_period_key = 'rebalance_period'

    # for all projects in the config data, iterate through and buld + populate a project object for each
    # with bloomberg data, additional csv data, window data, and global config data
    # and then return this list of populated projects
    projects: List[Project] = []
    for project_name, raw_project_config in config_data.items():

        logger.info(f"\n\nproject: {project_name}\n")
        # print("Windwo")
        # print(raw_project_config[window_key])
        input_window = Window.from_dict(raw_project_config[window_key])
        new_project = Project(project_name, input_window,
                              raw_project_config[rebalance_period_key])

        sectors_data = raw_project_config[sectors_key]
        for sector_type, raw_sector_config in sectors_data.items():
            logger.info(f"\n\nsector: {sector_type}\n")
            logger.info(f"Loading Bloomberg Data")

            if not SectorType.has_value(sector_type):
                raise ValueError(f'invalid sector type {sector_type} provided')
            sector_type_obj = SectorType(sector_type)

            predict = Predict.from_dict(
                sector_type_obj, raw_sector_config[predict_key])

            input_data = raw_sector_config[input_key]

            data_lag = input_data.get(lag_key, 0)
            new_sector = Sector(sector_type_obj, data_lag, predict)

            # create bloombergdata object that contains the loaded data (from Bloomberg API or from disk) and then store it in the project
            for tickername, raw_bloomberg_config in input_data.get(bloomberg_data_key, {}).items():
                current_bloomberg_data = BloombergData.from_dict(new_project, tickername,
                                                                 raw_bloomberg_config, args.bloomberg)
                new_sector.bloomberg_data[tickername] = current_bloomberg_data

            logger.info(f"Loading Additional Data")
            # create an additional data object full of the loaded data and then store it in the project
            for additional_name, raw_additional_config in input_data.get(additional_data_key, {}).items():
                current_additional_data = Additional.from_dict(new_project, additional_name,
                                                               raw_additional_config, args.additional)
                new_sector.additional_data[additional_name] = current_additional_data

            logger.info(f"Instantiating Operations")
            # Parses the operations
            for raw_operation_config in input_data.get(operations_key, []):
                current_operation = Operation(sector_type_obj, raw_operation_config[operations_output_columns_key],
                                              raw_operation_config[operation_type_key],
                                              raw_operation_config[operations_input_columns_key],
                                              raw_operation_config.get(
                                                  operations_arguments_key, {}),
                                              raw_operation_config.get(operations_remove_key, {}))
                new_sector.operations.append(current_operation)

            logger.info(f"Instantiating Models")
            # Parses the models
            for raw_model_config in raw_sector_config.get(models_key, []):
                model_type = raw_model_config[type_key]
                if not ModelType.has_value(model_type):
                    raise ValueError(
                        f'invalid model type {model_type} provided')
                # cast the string model_type to be an enum and store that into model_type_obj
                model_type_obj = ModelType(model_type)

                # current_model is a fully instantiated "Model Object", not trained but all of the attributes are set
                # if you run your train fuction in the constructor of your Model object then this WILL train your mdoel
                # if not, then it wont be trained
                current_model = model_type_map[model_type_obj].from_dict(
                    sector_type_obj, raw_model_config, input_window)
                new_sector.models.append(current_model)

            new_project.sectors[sector_type_obj] = new_sector

        optimize_data = raw_project_config[optimization_key]
        for optimization_type, raw_optimization_config in optimize_data.items():
            if not OptimizerType.has_value(optimization_type):
                raise ValueError(
                    f'invalid optimization type {optimization_type} provided')
            optimization_type_obj = OptimizerType(optimization_type)

            # TODO - create optimization type map with from dict etc
            # raw_optimization_config[benchmark_key]

            # iterate through benchmarks
            optimization_benchmark_data: Dict[str, CleanData] = {}
            for tickername, raw_bloomberg_config in raw_optimization_config[benchmark_key][input_key].get(bloomberg_data_key, {}).items():
                optimization_benchmark_data[tickername] = CleanData(project_name, SectorType.benchmark,
                                                                    {tickername: BloombergData.from_dict(new_project, tickername, raw_bloomberg_config, args.bloomberg)}, {}, 0, None, new_project, None, args.clean)

            raw_optimization_config[benchmark_key] = optimization_benchmark_data
            current_optimization = optimizer_type_map[optimization_type_obj].from_dict(
                raw_optimization_config)
            new_project.optimizations[optimization_type_obj] = current_optimization

        projects.append(new_project)

    # return the populated projects list
    return projects


if __name__ == "__main__":
    config_file_path = join(config_folder, argv[1])
    # print(read_config(config_file_path))
