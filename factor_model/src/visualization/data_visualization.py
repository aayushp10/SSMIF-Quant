#!/usr/bin/env python3
"""
    Visualize raw data and cleaned data taking special note of outliers and datapoints generated within recessions,
    during earnings season, and during each market regime we have entered since ~(1990-1995)
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

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.backends.backend_pdf
from utils.model_utils import get_file_list
from utils.model_utils import file_relative_path
from scipy.stats import norm
from os.path import join, basename
from constants import clean_data_folder, data_viz_folder
from dateutil.relativedelta import relativedelta
import datetime
from loguru import logger
from utils.error_handling import HandleErrors
from typing import List, Dict, Union, Any


def pretty_print(d: Dict, indent: int = 0) -> None:
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty_print(value, indent+1)
        else:
            print('\t' * (indent+1) + str(value))


@HandleErrors
def get_csv_paths() -> List[str]:
    glob_rel_path: str = join(clean_data_folder, "*.csv")
    return get_file_list(glob_rel_path, "foo")


def _get_col_mean(frame: pd.DataFrame, colname: str):
    return frame[colname].mean()


def _get_col_stdev(frame: pd.DataFrame, colname: str):
    return frame[colname].std()


def _get_col_variance(frame: pd.DataFrame, colname: str):
    return _get_col_stdev(frame, colname) ** 2


def _get_col_rolling(frame: pd.DataFrame, colname: str, window: int = 50):
    return frame[colname].rolling(50).mean()


def _get_col_pct_change_mean(frame: pd.DataFrame, colname: str):
    return frame[colname].pct_change(periods=1).mean()


def _get_col_pct_change_variance(frame: pd.DataFrame, colname: str):
    return _get_col_pct_change_stdev(frame, colname) ** 2


def _get_col_pct_change_stdev(frame: pd.DataFrame, colname: str):
    return frame[colname].pct_change(periods=1).std()


def _get_col_pct_change(frame: pd.DataFrame, colname: str):
    return frame[colname].pct_change(periods=1)


def _get_col_raw(frame: pd.DataFrame, colname: str):
    return frame[colname]


@HandleErrors
def calculate_stats(frame: pd.DataFrame, exclude: List[str] = ["date"]) -> Dict:
    """
    Return means, variances, stdevs, and the column names they are realted to 
    """
    # MUST PUT SCALAR VALUES FIRST OR THIS WILL NOT DISPLAY CORRECTLY
    # VALUES MUST BE NUMPY.FLOAT64
    # SERIES MUST BE SAVED AS PANDAS.CORE.SERIES.SERIES
    stats: List[str] = ["Mean", "Variance", "Standard Deviation", "Mean of Daily Pct Change", "Variance of Daily Pct Change",
                        "StDev of Daily Pct Change", "Simple Moving Average (50 days)", "Daily Percent Change", "Raw Column Data"]
    stat_calc_funcs: List[Any] = [_get_col_mean, _get_col_variance, _get_col_stdev, _get_col_pct_change_mean,
                                  _get_col_pct_change_variance, _get_col_pct_change_stdev, _get_col_rolling, _get_col_pct_change, _get_col_raw]
    output = dict()
    columns_of_interest = [col for col in frame.columns if col not in exclude]

    for column in columns_of_interest:
        statistics = dict()
        for stat, calc_func in zip(stats, stat_calc_funcs):
            statistics[stat] = calc_func(frame, column)

        output[column] = statistics

    output["null count"] = frame.isna().sum()

    return output


@HandleErrors
def plot_data(data: Dict, pdfname: str) -> None:
    """
    Plots the data input into it as a dictionary
    """
    pdf = matplotlib.backends.backend_pdf.PdfPages(f"{pdfname}Viz.pdf")
    fig, axes = plt.subplots(nclols=1, figsize=(16, 8))


@HandleErrors
def visualize_data(column_stats: Dict[str, Dict[str, Union[pd.core.series.Series, np.float64]]], name: str):
    logger.info(f"Visualizing data for: {name}")
    with matplotlib.backends.backend_pdf.PdfPages(file_relative_path(join(data_viz_folder, f'{name}_visualization.pdf'))) as pdf:
        # Title for the whole figure
        plt.figure()
        plt.axis('off')
        plt.text(0.5, 0.5, name, ha='center', va='top')
        pdf.savefig()
        plt.close()

        # for all of the columns
        for item, value in column_stats.items():
            logger.info(item)

            isScalar: bool = True
            plt.figure()
            plt.axis('off')
            plt.title(item)
            cell_text = []
            row_labels = []
            combination_values = []
        # for all of the stats about those columns
            for i, v in value.items():
                # if no longer a scalar stat
                if type(v) == pd.core.series.Series:
                    continue
                # if still a scalar stat
                cell_text.append([f"{v}"])
                row_labels.append([f"{i}"])
            plt.table(cellText=cell_text, rowLabels=row_labels, colLabels=[
                      item], loc='center right').scale(0.5, 1.5)
            pdf.savefig()
            plt.close()

            for i, v in value.items():
                # if a scalar set
                if type(v) != pd.core.series.Series:
                    continue
                combination_values.append(v)
                plt.figure()
                plt.title(f"{i} raw")
                sns.set_style('darkgrid')
                sns.lineplot(data=pd.DataFrame(v), legend='full')
                pdf.savefig()
                plt.close()

                plt.figure()
                plt.title(f"{i} distplot")
                sns.set_style('darkgrid')
                sns.distplot(a=v, bins=15)
                pdf.savefig()
                plt.close()

            # And now all together
            plt.figure()
            plt.title("Combination Graph")
            sns.set_style('darkgrid')
            sns.lineplot(data=pd.DataFrame(value),
                         legend='brief', dashes=False)
            pdf.savefig()
            plt.close()
    logger.success(f"Completed visualization for: {name}")


def main():
    logger.info("\n\nINITIATING DATA VISUALIZATION\n")
    filepaths: List[str] = get_csv_paths()
    for filepath in filepaths:
        frame: pd.DataFrame = pd.read_csv(filepath)
        pct_change_frame: pd.DataFrame = frame.drop(
            columns=["date"]).pct_change()
        column_stats: Dict = calculate_stats(frame)
        pct_change_stats: Dict = calculate_stats(pct_change_frame)
        name: str = filepath.split('/')[-1].replace('.csv', '')
        visualize_data(column_stats, name)
    logger.success("\n\nDATA VISUALIZATION COMPLETE\n")


if __name__ == "__main__":
    main()
