#!/usr/bin/env python3
"""
    Additional encapsulation
"""
# import the necessary packages
from __future__ import annotations
import pandas as pd
from utils.utils import load_dataframe_sanitize, relative_file_path
from utils.enums import DataSource
from .global_config_data import GlobalConfigData
from .base_data import BaseData
from typing import List, Dict, Optional, Any
from os.path import isabs
from constants import columns_key, file_base_name_override_key, column_map_key


class Additional(BaseData):

    # specify the data source type as additional/arbitrary data
    data_source_type = DataSource.additional

    # initialize the parameters for additional data by utilizing inheritance from the base data class
    def __init__(self,
                 global_config: GlobalConfigData,
                 name: str,
                 input_path: str,
                 columns: List[str],
                 col_map: List[Dict[str, str]],
                 override_basename: Optional[str] = None,
                 load_only_fs: bool = False):

        # if the path is absolute, store that as the input path, otherwise utilize the relative_file_path
        # function in order to get the file path relative to the current directory
        self.input_path = input_path if isabs(
            input_path) else relative_file_path(input_path)
        super().__init__(global_config, name, columns,
                         col_map, override_basename, load_only_fs)

    @classmethod
    def from_dict(cls, global_config: GlobalConfigData, name: str, input_dict: Dict[str, Any], load_only_fs: bool) -> Additional:
        """
        constructor for additional data from dict
        """
        input_path_key = 'input_path'
        return cls(global_config, name,
                   input_dict[input_path_key],
                   input_dict[columns_key],
                   input_dict.get(column_map_key, []),
                   input_dict.get(file_base_name_override_key),
                   load_only_fs)

    def _load_dataset(self, global_config: GlobalConfigData) -> pd.DataFrame:
        return load_dataframe_sanitize(self.input_path)
