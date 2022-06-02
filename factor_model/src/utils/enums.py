#!/usr/bin/env python3
"""
Enum objects (better than strings)
"""
from enum import Enum
from typing import Set, Any
from utils.steps import StepType


class BaseEnum(Enum):
    @classmethod
    def has_value(cls, value: str) -> bool:
        """
        Return true / false for whether the input is stored as a value in the enum
        """
        return value in cls.__members__

    @classmethod
    def get_values(cls) -> Set[Any]:
        """
        Return a list of the values stored within the enum
        """
        return set(item.value for item in cls)


class ModelType(BaseEnum):
    """
    Enum to store ml model type
    """
    linear_regression = "linear_regression"
    random_forest = 'random_forest'
    arima_regression = 'arima_regression'


class OptimizerType(BaseEnum):
    """
    Enum to store optimzier type
    """
    black_litterman = "black_litterman"
    hrp = "hrp"


class DataSource(BaseEnum):
    """
    Enum to store data source types
    """
    bloomberg = 'bloomberg'
    additional = 'additional'
    operations = 'operations'


class SectorType(BaseEnum):
    """
    Enum to store sectors
    """
    tech = 'tech'
    hlth = 'hlth'
    cond = 'cond'
    tels = 'tels'
    fin = 'fin'
    indu = 'indu'
    cons = 'cons'
    util = 'util'
    matr = 'matr'
    eng = 'eng'
    benchmark = 'benchmark'


class TimeScale(BaseEnum):
    """
    time scale
    """
    day = 'D'
    week = 'W'
    month = 'M'
    year = 'Y'
