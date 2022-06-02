#!/usr/bin/env python3
"""
    Operations object
"""
import pandas as pd
import numpy as np

from enum import Enum
from collections.abc import Iterable
from typing import Callable, Dict, Tuple, List, Any, Optional

from utils.enums import BaseEnum, TimeScale


def take_ratio(data: pd.DataFrame) -> Tuple[Iterable]:
    """
    datapath, outputcols, inputcols, kwargs
    """
    ratio = data[data.columns[0]] / data[data.columns[1]]

    return ratio,


def add_from_additional(data: pd.DataFrame) -> Tuple[Iterable]:
    """
    Function used as a bridge between specific columns in an additional dataframe, and the main training .csv for a project
    """
    columns: List[pd.Series] = []
    for col in data.columns:
        columns.append(data[col])

    return data,


class FunctionType(BaseEnum):
    """
    Enum to store valid function types
    """
    take_ratio = 'take_ratio'


function_map: Dict[FunctionType, Callable] = {
    FunctionType.take_ratio: take_ratio,
}
