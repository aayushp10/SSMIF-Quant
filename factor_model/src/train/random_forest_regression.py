#!/usr/bin/env python3
"""
    Random Forest Regression to project price / a price derivative
"""
# import the necessary packages
from __future__ import annotations
import pandas as pd
from os.path import basename
from loguru import logger
from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from classes.predict import PredictData
from utils.enums import ModelType, SectorType
from operations.run_operations import RunOperations
from typing import Any, List, Optional, Dict
from .base_model import BaseModel
import numpy as np
from classes.window import Window
import pickle


class RandomForest(BaseModel):

    # set the model type as a random forest
    model_type = ModelType.random_forest
    model: Optional[RandomForestRegressor] = None
    # initialize the necessary parameters for the random forest model while using super to initialize them from the sklearn model class

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
        train the random forest model from the operated data
        """

        if load_only_fs:
            self.load_model()
            return

        logger.info("\n\nINITIATING RANDOM FOREST REGRESSION\n")
        logger.info(
            f'Creating {self.model_type} model for {operations_data.basename}')

        # save the operated data as a pandas dataframe
        df: pd.Dataframe = operations_data.data

        # Drop all rows with nan values
        df: pd.Dataframe = df.dropna()

        # Generate the train test split for the random forest regression using SkLearn
        # TODO we have to make this so it isn't the basic sklearn one
        columns: List[str] = [col.normalize_colname()
                              for col in self.predictors]
        target_column = predict.target.normalize_colname()
        for column in [*columns, target_column]:
            if column not in df:
                raise ValueError(
                    f'cannot find column {column} in the dataframe')

        X_train, X_test, y_train, y_test = train_test_split(
            df[columns], df[target_column], shuffle=False)

        # Define and Fit the model in order to obtain the R^2 score
        # TODO - figure out and comment the type of score that is being generated
        # print(self.hyper_parameters)
        forest = RandomForestRegressor(**self.hyper_parameters)

        forest.fit(X_train, y_train)
        score = forest.score(X_test, y_test)
        logger.success(f"score : {score}")

        # Generate the Mean Squared Error for the testing set
        self.error = metrics.mean_squared_error(y_test, forest.predict(X_test))
        logger.success(f"MSE : {self.error}")

        # Save the model to disk
        self.model = forest
        self.save_model()

        logger.success("Model successfully saved to disk")

    def predict(self, data: Optional[List[float]] = None, window: Optional[Window] = None) -> Tuple[List[float], float]:
        """
        run prediction
        """
        logger.info('random forest')
        if data is None:
            raise ValueError('no data provided')
        predictions = self.model.predict(data)
        return np.array(predictions).flatten(), self.error
