#!/usr/bin/env python3
"""
Operations object
"""

import pandas as pd

from loguru import logger
from typing import List, Any
from os.path import join, exists

from classes.operation import Operation
from classes.global_config_data import GlobalConfigData

from .operations_functions import function_map

from utils.utils import load_dataframe_sanitize, normalize_str

from constants import operated_data_folder


class RunOperations:

    def __init__(self,
                 global_config: GlobalConfigData,
                 clean_data: Any,
                 operations: List[Operation],
                 load_only_fs: bool = False):
        self.basename = f"{normalize_str(global_config.project)}.csv"
        self.data = self._run_operations(
            clean_data.data, operations, load_only_fs)
        self.operations = operations

    def getOperations():
        return self.operations

    def get_file_path(self) -> str:
        return join(operated_data_folder, self.basename)

    def _run_operations(self, data: pd.DataFrame, operations: List[Operation], load_only_fs: bool) -> pd.DataFrame:
        """
        run list of operations on the data
        """
        file_path = self.get_file_path()
        if load_only_fs:
            if not exists(file_path):
                raise ValueError(f'could not find file {file_path}')
            return load_dataframe_sanitize(file_path)

        for operation in operations:
            # input columns = [normalize_colname(colname) for colname in operation.input_columns]
            # same thing if list comprehensions are your thing
            input_columns = [input_column.normalize_colname()
                             for input_column in operation.input_columns]
            # run the functions
            output_data = function_map[operation.type](
                data[input_columns], **operation.arguments)
            # print(operation.output_columns[1].column_name)

            if not isinstance(output_data, tuple):
                raise ValueError(
                    f'output of operation {operation.type.name} must be a tuple')

            # print(output_data)
            for i, current_output_data in enumerate(output_data):
                # print(operation.output_columns[1].name)
                # print(f"Length of new data: {current_output_data}, Length of old dataset {data}")
                for i, column in enumerate(current_output_data):
                    # print(operation.output_columns[1].name)
                    if len(current_output_data[i]) != len(data):
                        raise ValueError(
                            f'length of output for operation {operation.type.name} != length of dataframe')
                    # print(operation.output_columns[1].name)
                    data[operation.output_columns[i].normalize_colname()
                         ] = current_output_data[i]

            for remove_column_name in operation.remove:
                del data[remove_column_name]

        logger.success('done with all operations')
        # print(data)
        data.to_csv(file_path)

        return data
