#!/usr/bin/env python3
"""
Additional encapsulation
"""
# Import necessary packages
from __future__ import annotations
from abc import ABCMeta, abstractmethod
import pandas as pd
from os import makedirs
from os.path import join, exists
from typing import List, Dict, Optional

from loguru import logger
from classes.global_config_data import GlobalConfigData
from utils.error_handling import HandleErrors
from utils.utils import map_columns, normalize_str, \
    load_dataframe_sanitize, data_source_prepend_map, relative_file_path
from constants import date_key, raw_data_folder


class BaseData(metaclass=ABCMeta):
    filename_split_char: str = '_'

    # Initialize parameters for the Base Data class
    def __init__(self, global_config: GlobalConfigData, name: str, columns: List[str],
                 col_map: List[Dict[str, str]], override_basename: Optional[str] = None,
                 load_only_fs: bool = False):
        self.name = name
        self.columns = columns
        self.col_map = col_map
        # generate a basename for the data: if one is provided, use that, otherwise, set the basename to the normalized name for the data
        self.basename = override_basename if override_basename is not None \
            else f"{normalize_str(self.name)}.csv"
        self.data = self._load_data(global_config, load_only_fs)

    @property
    @abstractmethod
    def data_source_type(self):
        """
        data source type
        """
        pass

    @staticmethod
    def get_folder_path(project_name: str) -> str:
        return relative_file_path(join(raw_data_folder, project_name))

    def get_file_path(self, folder_path: str) -> str:
        path_prepend = data_source_prepend_map[self.data_source_type]
        return join(folder_path, self.filename_split_char.join([path_prepend, self.basename]))

    @HandleErrors
    def _load_data(self, global_config: GlobalConfigData, load_only_fs: bool) -> pd.DataFrame:
        """
        whole point of this is to set the data property on obj
        """
        # get folder path for the project
        folder_path = self.get_folder_path(global_config.project)
        file_path = self.get_file_path(folder_path)

        # if you want to load from filesystem and the file does not exist: error
        # If you do not want to load the data from bloomberg API then use this
        # For additional, if you have the flag set that would imply that you
        # have run this or have the .csv file that you want so you want to load it
        # from wherever we auto save it. Otherwise if you run this we will go in
        # and save a copy of the cleaned version of your original csv so that later on
        # its stored here

        if load_only_fs:
            if not exists(file_path):
                raise ValueError(f'could not find file {file_path}')
            return load_dataframe_sanitize(file_path)

        # Load the data
        data: pd.DataFrame = self._load_dataset(global_config)

        # Change the column names to match the col_map laid out in the config
        for col_map in self.col_map:
            data = map_columns(data, col_map)

        # If the folder that we are supposed to save this to does not exist, create it
        if not exists(folder_path):
            makedirs(folder_path, exist_ok=True)

        # Save the data
        logger.info(f'columns: {data.columns}')
        logger.info(f'saving data to {file_path}')
        data.to_csv(file_path)

        return data

    @abstractmethod
    def _load_dataset(self, global_config: GlobalConfigData):
        pass
