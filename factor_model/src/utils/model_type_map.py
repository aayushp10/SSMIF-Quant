#!/usr/bin/env python3
"""
Enum objects (better than strings)
"""
from typing import Dict
from classes.model import Model
from .enums import ModelType

from train.random_forest_regression import RandomForest
from train.arima_regression import ArimaRegression
from train.linear_regression import LinearRegression

model_type_map: Dict[ModelType, Model] = {
    ModelType.linear_regression: LinearRegression,
    ModelType.random_forest: RandomForest,
    ModelType.arima_regression: ArimaRegression,
}
