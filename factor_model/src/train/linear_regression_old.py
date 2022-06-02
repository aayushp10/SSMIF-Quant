#!/usr/bin/env python3
"""
    Linear Regression to project price / a price derivative
"""
# Import necessary packages
from __future__ import annotations
import pandas as pd
from os.path import basename
from loguru import logger
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression as sklinreg
from classes.predict import PredictData
from utils.enums import ModelType, SectorType
from operations.run_operations import RunOperations
from typing import Any, List
from .base_model import BaseModel
from typing import Dict, List, Optional, Any
import numpy as np
from classes.window import Window


class LinearRegression(BaseModel):
    # Set Model Type to linear regression
    model_type = ModelType.linear_regression
    model: Optional[sklinreg] = None
    # Initialize the necessary parameters to Linear Regression class using super to initialize them from sklearn model class

    def __init__(self, name: str, sector_type: SectorType,
                 predictors: List[Dict[str, str]],
                 hyper_parameters: Dict[str, Any],
                 fit_parameters: Dict[str, Any],
                 training_window: Window):

        self.error: float = 0.
        super().__init__(name, sector_type, predictors,
                         hyper_parameters, fit_parameters, training_window)

    # Define methon to train linear regression from the operated data
    def train_model(self, predict: PredictData,
                    operations_data: RunOperations,
                    load_only_fs: bool = False) -> None:
        """
        train the linear regression model from the operated data
        """
        if load_only_fs:
            self.load_model()
            return

        logger.info("\n\nINITIATING LINEAR REGRESSION\n")
        logger.info(
            f'Creating {self.model_type} model for {operations_data.basename}')

        # Create dataframe df of operations data
        df: pd.Dataframe = operations_data.data

        # Drop all rows with nan values
        df: pd.Dataframe = df.dropna()

        # Train test split
        # TODO use a custom split function that doesnt shuffle the data
        columns: List[str] = [col.normalize_colname()
                              for col in self.predictors]
        target_column = predict.target.normalize_colname()
        # print(df.columns)
        for column in [*columns, target_column]:
            if column not in df:
                raise ValueError(
                    f'cannot find column {column} in the dataframe')

        X_train, X_test, y_train, y_test = train_test_split(
            df[columns], df[target_column], shuffle=False)
        # Define, fit, and score the regression: score = r^2
        linear = sklinreg(self.hyper_parameters)
        linear.fit(X_train, y_train)
        training_pred = linear.predict(X_test)
        self.error = metrics.r2_score(training_pred, y_test)

        logger.success(f'r^2 score: {self.error}')

        # Generate the mean squared error
        mse = metrics.mean_squared_error(y_test, linear.predict(X_test))
        logger.success(f'mean squared error: {mse}')

        # Display coefficients to the user
        coefficients = linear.coef_
        logger.success("")

        # Save model to disk
        self.model = linear
        self.save_model()

        logger.success("Model successfully saved to disk")

    def predict(self, data: Optional[List[float]] = None, window: Optional[Window] = None) -> Tuple[List[float], float]:
        """
        run prediction
        """
        logger.info('linear regression')
        if data is None:
            raise ValueError('no data provided')
        predictions = self.model.predict(data)
        return np.array(predictions).flatten(), self.error
