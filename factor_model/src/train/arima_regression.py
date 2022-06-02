#!/usr/bin/env python3
"""
ARIMA Regression to project price / a price derivative
"""
# import the necessary packages
from __future__ import annotations
import pandas as pd
import numpy as np
from loguru import logger
from statsmodels.tsa.arima.model import ARIMA
from sklearn import metrics
from classes.predict import PredictData
from utils.enums import ModelType, SectorType
from operations.run_operations import RunOperations
from .base_model import BaseModel
from typing import Dict, List, Optional, Any
from classes.window import Window


class ArimaRegression(BaseModel):
    """
    Create an Arima Regression object that inherits from the SkLearn model parent class.
    An Arima Regression is an autoregressive intrgrated moving average model that will predict something
    based on its own past behaviors and a moving average (in this case a rolling one, however this is customizable 
    with different hyperparameters)
    """
    # set the model type as an arima regression
    model_type = ModelType.arima_regression
    model: Optional[ArimaRegression] = None
    uses_window: bool = True

    # initialize the necessary parameters for the arima model while using super to initialize them from the sklearn model class
    def __init__(self, name: str, sector_type: SectorType,
                 predictors: List[Dict[str, str]],
                 hyper_parameters: Dict[str, Any],
                 fit_parameters: Dict[str, Any],
                 training_window: Window = None):

        self.error: float = 0.
        super().__init__(name, sector_type, predictors,
                         hyper_parameters, fit_parameters, training_window)

    def train_model(self, predict: PredictData,
                    operations_data: RunOperations,
                    load_only_fs: bool = False) -> None:
        """
        train the arima regression model from the operated data
        """
        if load_only_fs:
            self.load_model()
            return

        logger.info("\n\nINITIATING ARIMA REGRESSION\n")
        logger.info(
            f'Creating {self.model_type} model for {operations_data.basename}')

        # Generate the log data
        df_array = operations_data.data[predict.target.normalize_colname()]
        df_log = np.log(df_array)

        # Create the Arima Model by fitting it and lag the price
        arima = ARIMA(df_log, **self.hyper_parameters)
        arima_trained = arima.fit(**self.fit_parameters)

        # Get predictions for the arima model
        predictions_ARIMA = np.exp(arima_trained.fittedvalues)

        # Calculate the R^2 score for the ARIMA regression
        score = metrics.r2_score(df_array[1:], predictions_ARIMA[1:])
        logger.success(f'r^2 score: {score}')

        # Calculate the error for the ARIMA regression
        self.error = metrics.mean_squared_error(
            df_array[1:], predictions_ARIMA[1:])
        logger.success(f'mean squared error: {self.error}')

        # save the model to disk
        self.model = arima_trained
        self.save_model()

        logger.success("Model successfully saved to disk")

    def predict(self, data: Optional[List[float]] = None, window: Optional[Window] = None) -> Tuple[List[float], float]:
        """
        run prediction
        """
        logger.info('arima')
        if window is None:
            raise ValueError('no window provided')
        predictions = self.model.predict(
            start=window.start_date, end=window.start_date)
        return np.array(predictions).flatten(), self.error
