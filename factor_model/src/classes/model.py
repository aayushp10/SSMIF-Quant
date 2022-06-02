#!/usr/bin/env python3
"""
model class
"""
# Import necessary packages
from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import Dict, List, Any, Optional, Tuple

from utils.enums import ModelType, SectorType
from .window import Window
from .normalized_column import NormalizedColumn
from .predict import PredictData

from operations.run_operations import RunOperations


class Model(metaclass=ABCMeta):
    """
    Abstract Model class
    """
    # Initialize parameters for Model class

    def __init__(self, name: str, sector_type: SectorType,
                 predictors: List[Dict[str, str]],
                 hyper_parameters: Dict[str, Any],
                 fit_parameters: Dict[str, Any],
                 training_window: Window):

        self.name = name

        self.predictors: List[NormalizedColumn] = []

        # Append NormalizedColumn to predictors
        for predictor in predictors:
            self.predictors.append(
                NormalizedColumn.from_dict(sector_type, predictor))

        self.hyper_parameters: Dict[str, Any] = hyper_parameters
        self.fit_parameters: Dict[str, Any] = fit_parameters

        self.training_window: Window = training_window

    @classmethod
    def from_dict(cls, sector_type: SectorType, input_dict: Dict[str, Any], training_window: Window) -> Model:
        """
        constructor for model object from dict
        """
        name_key = 'name'
        predictors_key = 'predictors'
        hyper_parameters_key = 'hyperparams'
        fit_parameters_key: str = 'fitparams'
        # search_parameters_key = 'searchparams'

        return cls(input_dict[name_key], sector_type,
                   input_dict.get(predictors_key, []),
                   input_dict.get(hyper_parameters_key, {}),
                   input_dict.get(fit_parameters_key, {}), training_window)

    # This isn't actually a callable. it's an abstract property
    # in java you may have a class with: model_type = [] and then
    # inherit and set that in your children
    # same thing
    @property
    @abstractmethod
    def model(self):
        """
        the actual trained model
        """
        pass

    @property
    @abstractmethod
    def model_type(self):
        """
        the type of the given model (ModelType enum)
        """
        pass

    @property
    @abstractmethod
    def uses_window(self):
        """
        use window in predict
        """
        pass

    @abstractmethod
    def train_model(predict: PredictData, operations_data: RunOperations,
                    load_only_fs: bool = False) -> None:
        pass

    @abstractmethod
    def predict(self, data: Optional[List[float]] = None, window: Optional[Window] = None) -> Tuple[List[float], float]:
        """
        returns prediction of model with confidence level, passing in data or window, depending on the model
        """
        pass
