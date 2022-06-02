#!/usr/bin/env python3
"""
Helper functions for running our models
If this becomes too clunky we can merge this and dataload_utils
"""

import pandas as pd
from datetime import datetime

from glob import glob
from loguru import logger
from pathlib import Path
from joblib import dump, load
from bidict import bidict
from os.path import abspath, join, basename, splitext
from typing import Optional, Set, List, Any, Dict

from utils.enums import DataSource

from constants import date_format, non_numeric_cols, date_key, models_folder

# Tells you the prefixes given to columns loaded from
# each type of data source, ex: a column called px_last
# loaded from bloomberg will be prefixed with bb
# so the new name will be bb_px_last
data_source_prepend_map: bidict = bidict({
    DataSource.bloomberg: 'bb',
    DataSource.additional: 'add',
    DataSource.operations: 'op',
})


def map_columns(frame: pd.DataFrame, col_map: Dict[str, str]):
    """
    change the name of one column to another
    """
    old_key_key = 'old_key'
    new_key_key = 'new_key'
    return frame.rename(columns={col_map[old_key_key]: col_map[new_key_key]})


def normalize_str(name: str) -> str:
    """
    return normalized string for paths and such
    """
    return name.strip().replace(' ', '_').lower()


def relative_file_path(rel_path: str) -> str:
    """
    get file path relative to current directory
    """
    complete_path: str = join(
        abspath(join(Path(__file__).absolute(), '../../..')), rel_path)
    return complete_path


def load_dataframe_sanitize(file_path: str) -> pd.DataFrame:
    """
    load dataframe from disk and fix problems with columns
    """
    df: pd.DataFrame = pd.read_csv(file_path, index_col=None)
    numeric_columns = [
        col for col in df.columns if col not in non_numeric_cols]
    df[numeric_columns] = df[numeric_columns].apply(
        pd.to_numeric, errors='coerce')
    df[date_key] = pd.to_datetime(df[date_key], format=date_format)
    df = df.set_index(date_key)
    return df
