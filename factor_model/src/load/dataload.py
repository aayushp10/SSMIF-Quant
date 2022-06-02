#!/usr/bin/env python3
"""
    Loading data from bloomberg terminal and other sources
    Upon load the raw data will be saved to csv format in raw_data/
    The data will then be cleaned and saved in clean_data/

    We will duplicate data for ease of use within subsequent models - this point is up for debate

    We will load valuation and sentiment-approximating data from a series of sector ETFs
    We will load macroeconomic data
"""


# from loguru import logger
# #from dataclean import process_macroeconomic_files, process_sentiment_files
# import pdblp
# import pandas as pd
# from datetime import date
# from constants import macro_data_path, sentiment_data_path, sector_etfs, sentiment_fields, macroeconomic_indices, start_date, end_date
# from typing import List

# date_block_format: str = '%Y%m%d'


import numpy as np
import pandas as pd
from sys import argv
from typing import List
from loguru import logger

from classes.yf_data import YFData
from classes.read_config import read_config
from classes.bloomberg_data import BloombergData


def main(config_path: str):
    sectors = read_config(config_path)
    for sector in sectors:
        sector.load()


if __name__ == "__main__":
    main(argv[1])


# def load_dataset(dataset_names: List[str], dataset_valuation_fields: List[str], colnames: List[str], start_date: date,
#                  end_date: date, con, case: str =None) -> List[pd.DataFrame]:
#     """
#     :param dataset_names: list of dataset names to be passed into the con object : List[str]
#     :param dataset_valuation_fields: list of fields to pull for each dataset from the con object : List[str]
#     :param start_date: start date of the data : datetime.date
#     :param end_date: end date of the data : datetime.date
#     :param con: connector object for the pdblp api or a database connection object with a matching interface
#     :param case: controls special behavior of the function
#     :return: A list of dataframes corresponding to those requested with each valuation field as a column
#              in every dataset : List[pd.DataFrame]
#     """
#     output_data = []
#     i: int = 0
#     for index in dataset_names:
#         frame = con.bdh([index], dataset_valuation_fields, \
#             start_date.strftime(date_block_format), end_date.strftime(date_block_format))
#         if case == "macro":
#             frame.columns = ["PX_LAST"]
#         elif case != "macro":
#             frame.columns = colnames
#         output_data.append(frame)
#         i += 1
#     return output_data

# def write_datasets_to_file(paths: List[str], frames_lists: List[List[pd.DataFrame]], labels_list: List[str]) -> None:
#     """
#     :param paths: a list of filepaths
#     :param frames_lists: a list of lists of dataframes
#     """
#     for path, frames, labels in zip(paths, frames_lists, labels_list):
#         for frame, label in zip(frames, labels):
#             save_path: str = path.split(".csv")[0]
#             save_path += (label + ".csv")
#             with open(save_path, "w"):
#                 frame.to_csv(save_path)


# def load_data_from_bloomberg() -> None:
#     """
#     Load and save raw data from bloomberg
#     """

#     macroeconomic_data: List[pd.DataFrame] = []
#     sentiment_data: List[pd.DataFrame] = []

#     try:
#         logger.info("Attempting to estiablish connection with Bloomberg API")
#         con = pdblp.BCon(timeout=30000)
#         con.start()
#         logger.success("Connection Established")

#         logger.info("Loading macroeconomic Data")
#         macroeconomic_data = load_dataset(macroeconomic_indices, ['PX_LAST'], [], start_date, end_date, con, case="macro")
#         logger.info("Loading sentiment data")
#         sentiment_data = load_dataset(sector_etfs, sentiment_fields, sentiment_fields, start_date, end_date, con)

#         if len(sentiment_data) == 0 or len(macroeconomic_data) == 0:
#             raise ValueError("Unable to load some of the data, check Bloomberg API and internet connection")

#     except BaseException:
#         err = RuntimeError("Error loading datasets from blp, defaulting to existing data")
#         logger.error(err)
#         # raise err

#     try:
#         logger.info("Writing raw data to disk")
#         paths: List[str] = [macro_data_path, sentiment_data_path]
#         datasets: List[List[pd.DataFrame]] = [macroeconomic_data, sentiment_data]
#         labels: List[List[str]] = [macroeconomic_indices, sector_etfs]
#         write_datasets_to_file(paths, datasets, labels)

#     except FileNotFoundError:
#         err = RuntimeError("cannot find raw data folder")
#         logger.error(err)
#         raise err

# def main():
#     """ Load data from bloomberg and clean"""
#     logger.info("\n\nINITIATING DATA LOAD\n")
#     load_data_from_bloomberg()
#     logger.success("\n\nDATA LOAD COMPLETE\n")

# if __name__ == '__main__':
#     main()
