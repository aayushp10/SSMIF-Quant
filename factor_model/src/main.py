#!/usr/bin/env python3
"""
    Main entrypoint
"""
import argparse
import pandas as pd
from loguru import logger
from typing import Dict, List, Optional

# from visualization.data_visualization import main as dataviz
from clean.dataclean import CleanData

from classes.project import Project
from classes.bloomberg import BloombergData
from classes.operation import Operation
from classes.window import Window

from classes.factor_research import FactorResearch
from classes.read_config import read_config

# from classes.backtest import Backtest
from datetime import datetime, timedelta

from predict.predict import predict
from classes.backtest import Backtest
from utils.enums import OptimizerType, SectorType
from operations.run_operations import RunOperations
from copy import deepcopy
import matplotlib.pyplot as plt
from classes.regime_model import RegimeModel


def main():
    parser = argparse.ArgumentParser(description="SSMIF Factor Model")

    parser.add_argument("-b", "--bloomberg", default=False,
                        action="store_true", help="load bloomberg data from filesystem")
    parser.add_argument("-a", "--additional", default=False,
                        action="store_true", help="load additional data from filesystem")
    parser.add_argument("-c", "--clean", default=False,
                        action="store_true", help="load cleaned data from filesystem")
    parser.add_argument("-o", "--operations", default=False,
                        action="store_true", help="load additional data from operations")
    parser.add_argument("-t", "--train", default=False,
                        action="store_true", help="load training output from filesystem")
    parser.add_argument("-p", "--portfolio-optimization", default=True,
                        action="store_true", help="skip portfolio optimization")
    parser.add_argument("-r", "--predict", default=False,
                        action="store_true", help="skip run predictions")
    parser.add_argument("-v", "--viz", default=False,
                        action="store_true", help="run data visualization")
    parser.add_argument("-m", "--models-only", default=False,
                        action="store_true", help="just train and predict with the models")
    parser.add_argument("-f", "--full-backtest", default=False,
                        action="store_true", help="perform the full rebalanced backtest")
    parser.add_argument("--black-litterman", default=False, action="store_true",
                        help="compute the optimized portfolio using the black litterman model")
    parser.add_argument("--hrp", default=False, action="store_true",
                        help="compute the optimized portfolio using a hierarchical risk parity model")
    parser.add_argument("--regime-model", default=False, action="store_true",
                        help="compute the optimized portfolio using a hierarchical risk parity model")
    parser.add_argument("config", type=str,
                        help="path to config file from config folder")

    args = parser.parse_args()

    projects = read_config(args)

    '''
    
    '''

    if(args.models_only):
        sector_data = {}
        for project in projects:
            logger.info("Cleaning data")
            all_predictions: Dict[SectorType, List[float]] = {}
            i = 0
            for sector_type, sector in project.sectors.items():
                logger.info(f"Processing sector {sector_type.name}")
                clean_data = CleanData(project.name, sector_type, sector.bloomberg_data, sector.additional_data,
                                       sector.lag, sector.predict.target, project, args.clean)
                sector_data[sector_type] = clean_data
                if args.viz:
                    # TODO - fix data visualization
                    # dataviz()
                    print("viz")
                logger.info(f"Running Operations")
                run_operations = RunOperations(
                    project, clean_data, sector.operations, args.operations)

                logger.info(f"Initating training")
                for model in sector.models:
                    # if model.name == 'LinearRegression':
                    model.train_model(
                        sector.predict, run_operations, args.train)
                logger.success("Training Successful")

                predicted_results = predict(project, sector, clean_data, None)
                all_predictions[sector_type] = predicted_results
                # i = i+1
                # if i == 3:
                #     exit()

    elif (args.full_backtest):

        for project in projects:

            '''
            flip rembalnce loop with sector loop 
            train
            predict
            optimize => send weights to backtest
            backtest => get cumulative return lists as the return of the backtest that we keep track of to use at the end
            repeat
            '''

            '''
            TODO
            change clean data indexing so that we don't throw away end data and instead we throw away the old data
            '''

            rebalance_period = project.rebalance_period
            logger.info(f"Cleaning data")
            all_predictions: Dict[SectorType, List[float]] = {}
            sector_data: Dict[SectorType, CleanData] = {}

            backtest_cumulative_returns_by_optimizer_type: Dict[OptimizerType, Dict[str, List[float]]] = {
            }
            port_returns_key: str = 'port_returns'
            benchmark_returns_key: str = 'benchmark_returns'

            all_sectors = []
            for sector_type, sector in project.sectors.items():
                clean_data = CleanData(project.name, sector_type, sector.bloomberg_data, sector.additional_data,
                                       sector.lag, sector.predict.target, project, None, args.clean)
                sector_data[sector_type] = clean_data
                all_sectors.append(sector_type)

            # sector type is cast to string
            weights_data: Dict[datetime, Dict[str, float]] = {}

            num_rebalances = len(
                sector_data[all_sectors[0]].data) // rebalance_period

            for i in range(0, num_rebalances):
                logger.info(f"ON REBALANCE ITERATION : {i}")
                current_all_predictions: Dict[SectorType, List[float]] = {}

                first_sector_data = sector_data[all_sectors[0]].data

                training_window: Optional[Window] = None
                if((rebalance_period*(i)) + rebalance_period > len(sector_data[all_sectors[0]].data.index)):
                    training_window = Window(first_sector_data.index[max(
                        0, (i-1) * rebalance_period)], first_sector_data.index[-1])
                else:
                    training_window = Window(first_sector_data.index[max(
                        0, (i-1) * rebalance_period)], first_sector_data.index[(i+1)*rebalance_period])

                new_clean_data_per_sector: Dict[SectorType,
                                                Tuple[CleanData, NormalizedColumn]] = {}
                for sector_type, sector in project.sectors.items():
                    # clean_data = CleanData(project.name, sector_type, sector.bloomberg_data, sector.additional_data,
                    #                   sector.lag, sector.predict.target, None, args.clean)
                    # sector_data[sector_type] = clean_data

                    new_clean_data = deepcopy(sector_data[sector_type])
                    logger.info(
                        f'new clean data shape: {new_clean_data.data.shape}')
                    # if new_clean_data.lag:
                    # 0 - 180
                    # 0 - 360
                    new_clean_data.lagged_data = new_clean_data.lagged_data.iloc[max(
                        0, (i-1) * rebalance_period): (i + 1) * rebalance_period]
                    new_clean_data.data = new_clean_data.data.iloc[max(
                        0, (i-1) * rebalance_period): (i + 1) * rebalance_period]

                    new_clean_data_per_sector[sector_type] = new_clean_data, sector.predict.target
                    logger.info(
                        f'iteration {i}. data shape: {new_clean_data.data.shape}, head:\n{new_clean_data.data.head()}')

                    run_operations = RunOperations(
                        project, new_clean_data, sector.operations, args.operations)

                    sector.predict.output_window.start_date = new_clean_data.data.index[-1] - timedelta(
                        days=30)
                    sector.predict.output_window.end_date = new_clean_data.data.index[-1]
                    for model in sector.models:
                        model.training_window = training_window
                        model.train_model(
                            sector.predict, run_operations, args.train)

                    predicted_results = predict(
                        project, sector, new_clean_data, run_operations)
                    current_all_predictions[sector_type] = predicted_results

                weights_window: Optional[Window] = None

                if((rebalance_period * (i+1)) + rebalance_period > len(sector_data[all_sectors[0]].data.index)):
                    weights_window = Window(first_sector_data.index[(
                        i + 1) * rebalance_period], first_sector_data.index[-1])
                else:
                    weights_window = Window(first_sector_data.index[(
                        i + 1) * rebalance_period], first_sector_data.index[(i + 2) * rebalance_period])

                for optimizer_type, optimizer in project.optimizations.items():
                    optimizer.run_optimization(
                        current_all_predictions, new_clean_data_per_sector)
                    logger.success(
                        f"Optimization complete for {optimizer_type.name}. Output weights: {optimizer.weights}")

                    for current_day in pd.date_range(start=weights_window.start_date, end=weights_window.end_date):
                        if current_day not in weights_data:
                            weights_data[current_day] = {}
                        for sector in all_sectors:
                            if sector not in optimizer.weights['SPX Index']:
                                raise RuntimeError(
                                    f'sector {sector} not found in benchmark')
                            weights_data[current_day][sector] = optimizer.weights['SPX Index'][sector]

            weights_by_date = pd.DataFrame.from_dict(
                data=weights_data, orient='index', columns=all_sectors)

            for optimizer_type, optimizer in project.optimizations.items():
                backtester: Backtest = Backtest(
                    project, sector_data, {}, optimizer.benchmark)
                port_cumulative_returns, benchmark_cumulative_returns = backtester.run_backtest_on_df(
                    weights_by_date)
                backtest_cumulative_returns_by_optimizer_type[optimizer_type] = {
                }
                backtest_cumulative_returns_by_optimizer_type[optimizer_type][
                    port_returns_key] = port_cumulative_returns
                backtest_cumulative_returns_by_optimizer_type[optimizer_type][
                    benchmark_returns_key] = benchmark_cumulative_returns

                # if (optimizer_type not in list(backtest_cumulative_returns_by_optimizer_type.keys())):
                #     base = {}
                #     base[port_returns_key] = []
                #     base[benchmark_returns_key] = []
                #     backtest_cumulative_returns_by_optimizer_type[optimizer_type] = base

                # bl_cumlative_returns, spy_cumulative_returns_list = backtester.run_backtest(
                #     1 if len(backtest_cumulative_returns_by_optimizer_type[optimizer_type][port_returns_key]) == 0 else backtest_cumulative_returns_by_optimizer_type[optimizer_type][port_returns_key][-1],
                #     1 if len(backtest_cumulative_returns_by_optimizer_type[optimizer_type][benchmark_returns_key]) == 0 else backtest_cumulative_returns_by_optimizer_type[optimizer_type][benchmark_returns_key][-1]
                # )
                # backtest_cumulative_returns_by_optimizer_type[optimizer_type][port_returns_key].extend(bl_cumlative_returns)
                # backtest_cumulative_returns_by_optimizer_type[optimizer_type][benchmark_returns_key].extend(spy_cumulative_returns_list)

            for optimizer_type, optimizer in project.optimizations.items():
                if optimizer_type == OptimizerType.black_litterman:
                    logger.success(
                        f"Complete Backtest Finished: \n Port Returns: ${backtest_cumulative_returns_by_optimizer_type[optimizer_type][port_returns_key]} \n Benchmark Return: ${backtest_cumulative_returns_by_optimizer_type[optimizer_type][benchmark_returns_key]}")
                    plt.plot(backtest_cumulative_returns_by_optimizer_type[optimizer_type]
                             [port_returns_key], color="green", label="Factor Model Returns")
                    plt.plot(backtest_cumulative_returns_by_optimizer_type[optimizer_type]
                             [benchmark_returns_key], color="black", label="S&P 500 Returns")
                    plt.title("Factor Model Returns vs. S&P 500 Returns")
                    plt.legend()
                    plt.ylabel('Cumulative Returns')
                    plt.savefig("visualizations/Backtest-Fig-Labeled2.png")

    elif(args.regime_model):
        pass
        # {
        #     "high_vol": [
        #         {
        #             "start_date": "2016-01-01"
        #             "start_date": "2016-04-24"
        #         },
        #         {
        #             "start_date": "2016-01-01"
        #             "start_date": "2016-04-24"
        #         },
        #     ]
        #     "low_vol": [
        #         {
        #             "start_date": "2016-01-01"
        #             "start_date": "2016-04-24"
        #         },
        #         {
        #             "start_date": "2016-01-01"
        #             "start_date": "2016-04-24"
        #         },
        #     ]
        # }
        # sector_data = {}
        # project = projects[0]
        # benchmark_data = (list(project.optimizations.values())[0].benchmark)
        # benchmark_data = benchmark_data[list(benchmark_data.keys())[0]]
        # regime = RegimeModel(benchmark_data)
        # regime.highVolatilityProbabilities()
        # regime.visualize_regimes()

    else:
        sector_data: Dict[str, CleanData] = {}
        for project in projects:
            logger.info(f"Cleaning data")
            all_predictions: Dict[SectorType, List[float]] = {}
            for sector_type, sector in project.sectors.items():
                logger.info(f"Processing sector {sector_type.name}")
                clean_data = CleanData(project.name, sector_type, sector.bloomberg_data, sector.additional_data,
                                       sector.lag, sector.predict.target, project, args.clean)
                sector_data[sector_type] = clean_data, sector.predict.target
                if args.viz:
                    # TODO - fix data visualization
                    # dataviz()
                    print("viz")
                logger.info(f"Running Operations")
                run_operations = RunOperations(
                    project, clean_data, sector.operations, args.operations)

                logger.info(f"Initating training")
                for model in sector.models:
                    # TODO - make the model classes for training
                    model.train_model(
                        sector.predict, run_operations, args.train)
                logger.success("Training Successful")

                if not args.predict:
                    # run the predict functions
                    predicted_results = predict(
                        project, sector, clean_data, None)
                    # for i in range(len(predicted_results)):
                    #     date = clean_data.lagged_data.index[-len(predicted_results)]
                    all_predictions[sector_type] = predicted_results

            # factor_research = FactorResearch(sector_data)
            # factor_research.run_factor_research()
            # exit()

            # backtest = Backtest(sector_data)
            # backtest.run_backtest()

            if args.portfolio_optimization:
                logger.info(f"Initiating Optimization")
                if len(project.optimizations) == 0:
                    raise ValueError("Must include at least one optimizer")

                for optimizer_type, optimizer in project.optimizations.items():
                    optimizer.run_optimization(all_predictions, sector_data)
                    logger.success(
                        f"Optimization complete for {optimizer_type.name}. Output weights: {optimizer.weights}")

    logger.success("\n\nFactor Model Complete\n")


if __name__ == "__main__":
    main()
