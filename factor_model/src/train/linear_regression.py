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
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA


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
        self.pc = hyper_parameters["pc"]
        super().__init__(name, sector_type, predictors,
                         hyper_parameters, fit_parameters, training_window)

    def scale_reduce_dimension(self, df):
        delta_size = self.pc - df.shape[0]
        if delta_size > 0:
            for _ in range(delta_size):
                df.loc[df.index.values[-1] +
                       np.timedelta64(1, 'D')] = df.iloc[-1]

        target_column = self.target_column
        columns: List[str] = [col.normalize_colname()
                              for col in self.predictors]
        scaler = MinMaxScaler(feature_range=(1, 10))
        scaler.fit(df)
        df = pd.DataFrame(scaler.transform(df), columns=df.columns)

        target_df = None if self.target_column not in df else df[self.target_column]

        pca = PCA(n_components=self.pc)
        pca.fit(df)
        df = pd.DataFrame(pca.transform(df), columns=[
                          f"predictor_{i}" for i in range(0, self.pc)])

        return df, target_df

        # if(self.target_column in list(df.columns)):
        #     targetDf = df[self.target_column]
        #     predictorsDf = df[list(filter(lambda c : c != target_column, columns))]
        #     pca = PCA(n_components=5)
        #     pca.fit(predictorsDf)
        #     df = pd.DataFrame(pca.transform(predictorsDf), columns=[f"predictor_{i}" for i in range(0,5)])
        #     df[target_column] = targetDf
        #     return df
        # else:
        #     pca = PCA(n_components=6)
        #     pca.fit(df)
        #     df = pd.DataFrame(pca.transform(df), columns=[f"predictor_{i}" for i in range(0,6)])
        #     return df

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

        columns: List[str] = [col.normalize_colname()
                              for col in self.predictors]
        target_column = predict.target.normalize_colname()
        self.target_column = target_column
        # Create dataframe df of operations data
        df: pd.Dataframe = operations_data.data

        # Drop all rows with nan values
        df: pd.Dataframe = df.dropna()
        target_df = df[target_column]
        df, target_df = self.scale_reduce_dimension(df)
        # Train test split
        # TODO use a custom split function that doesnt shuffle the data

        # print(df.columns)
        # for column in [*columns, target_column]:
        #     if column not in df:
        #         raise ValueError(f'cannot find column {column} in the dataframe')
        train_df = df[[f"predictor_{i}" for i in range(0, self.pc)]]
        X_train, X_test, y_train, y_test = train_test_split(
            train_df, target_df, shuffle=False)
        # Define, fit, and score the regression: score = r^2
        linear = sklinreg(self.hyper_parameters)
        linear.fit(X_train, y_train)
        training_pred = linear.predict(X_test)
        self.error = metrics.r2_score(training_pred, y_test)
        logger.success(f"--------{target_column} R^2 is {self.error}--------")

        # exit()
        # logger.success(f'r^2 score: {self.error}')

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

    def predict(self, data: Optional[pd.DataFrame] = None, window: Optional[Window] = None) -> Tuple[List[float], float]:
        """
        run prediction
        """
        logger.info('linear regression')
        if data is None:
            raise ValueError('no data provided')
        data.dropna()
        print(data)
        df, _ = self.scale_reduce_dimension(data)
        predictions = self.model.predict(df)

        return np.array(predictions).flatten(), self.error
