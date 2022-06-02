#!/usr/bin/env python3
"""
Bloomberg function encapsulation
"""
from __future__ import annotations
import pandas as pd
from loguru import logger
from classes.global_config_data import GlobalConfigData
from classes.base_data import BaseData
from utils.utils import DataSource
from typing import List, Dict, Optional, Any
from constants import date_key, columns_key, file_base_name_override_key, column_map_key


class BloombergData(BaseData):
    data_source_type = DataSource.bloomberg

    def __init__(self, global_config: GlobalConfigData,
                 tickername: str,
                 columns: List[str],
                 col_map: List[Dict[str, str]],
                 override_basename: Optional[str] = None,
                 load_only_fs: bool = False):
        # Data is loaded on creation of the bloomberg object and then stored in self.data
        # It is also saved to disk simultaneously
        super().__init__(global_config, tickername, columns,
                         col_map, override_basename, load_only_fs)

    @classmethod
    def from_dict(cls, global_config: GlobalConfigData, name: str, input_dict: Dict[str, Any], load_only_fs: bool) -> BloombergData:
        """
        constructor for bloomberg data from dict
        """
        return cls(global_config, name,
                   input_dict[columns_key],
                   input_dict.get(column_map_key, []),
                   input_dict.get(file_base_name_override_key),
                   load_only_fs)

    def _load_dataset(self, global_config: GlobalConfigData) -> pd.DataFrame:
        # Attempt bloomberg connection
        try:
            import pdblp
        except ModuleNotFoundError:
            logger.error("Unable to find pdblp module. env error")

        try:
            connection = pdblp.BCon(timeout=30000)
            connection.start()
        except Exception as err:
            logger.error("Unable to establish connection with Bloomberg API")
            raise err

        # Load the data from bloomberg
        date_block_format: str = '%Y%m%d'

        data = self._load_dataset_bloomberg(
            connection, [self.name], self.columns, global_config)

        return data

    def _load_dataset_bloomberg(self, connection: pdblp.BCon, ticker_names: List[str], columns: List[str], global_config: GlobalConfigData) -> pd.DataFrame:
        """
        :param dataset_name: list of dataset names to be passed into the con object : List[str]
        :param cols: list of fields to pull for each dataset from the con object : List[str]
        :return: A dataframe containing the data from bloomberg
        """
        date_block_format: str = '%Y%m%d'
        df = connection.bdh(ticker_names, columns, global_config.window.start_date.strftime(
            date_block_format), global_config.window.end_date.strftime(date_block_format))

        df = self.fix_dataframe(df)

        return df

    @staticmethod
    def fix_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """
        dataframe with 3 header rows is converted to 1
        """
        new_columns: List[str] = df.columns.get_level_values(1).values
        dates = df.index
        df = pd.DataFrame(df.values, columns=new_columns)
        df[date_key] = dates
        df = df.set_index(date_key)

        return df
