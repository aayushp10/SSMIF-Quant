#!/usr/bin/env python3
"""
predict
"""

import pandas as pd
import numpy as np
from loguru import logger
from typing import cast, List, Dict, Optional
import matplotlib.pyplot as plt
from scipy.special import softmax
from classes.project import Project
from classes.model import Model
from clean.dataclean import CleanData
from constants import date_key
from utils.error_handling import HandleErrors
from datetime import timedelta
import numpy as np
from classes.sector import Sector
from classes.global_config_data import GlobalConfigData
from classes.window import Window
from operations.run_operations import RunOperations


@HandleErrors
def predict(global_config: GlobalConfigData, sector: Sector, clean_data: CleanData, run_operations: Optional[RunOperations]) -> List[float]:
    """
    predict the stock prices
    """
    if not sector.predict.data.same_as_train:
        clean_data = CleanData(global_config.project, sector.sector,
                               project.predict.bloomberg_data, project.predict.additional_data)
        # extrapolate data up to the last predict day
        clean_data.extrapolate_to_date(sector.predict.output_window.end_date)
        if run_operations != None:
            run_operations = RunOperations(
                global_config.project, clean_data, sector.sector, run_operations.getOperations())

    # data = run_operations.data if run_operations != None else clean_data.data
    if run_operations != None:
        data = run_operations.data
    else:
        data = clean_data.lagged_data if clean_data.lag != None else clean_data.data

    window_size_days = timedelta(days=sector.predict.window_size)

    result: List[float] = []
    # print(data)
    # https://fda.readthedocs.io/en/latest/auto_examples/plot_extrapolation.html
    # to just do a model.predict you need defined x data, but ours ends at wahtever day it does
    # to be able to predict into the future we need to extrapolate out the trend lines that we have developed
    # and we can no longer just call model.predict
    # either that or we time lag all of the input data by delta at which point we can predict delta into the future

    num_days_predict: timedelta = sector.predict.output_window.end_date - \
        sector.predict.output_window.start_date

    for i in range(num_days_predict.days, -1, -1):

        predictions: List[float] = []
        errors: List[float] = []

        for model in sector.models:
            # cast
            model: Model = cast(Model, model)
            columns = [col.normalize_colname() for col in model.predictors]

            current_start = sector.predict.output_window.end_date - \
                timedelta(days=i)
            logger.info(f'predicting for {current_start}')
            rows = data.loc[current_start: current_start +
                            window_size_days, columns]

            # try:

            current_predictions, error = model.predict(window=Window(
                rows.index[0], rows.index[-1])) if model.uses_window else model.predict(data=rows)
            # except:
            #     print(sector.sector)
            #     print(current_start)
            #     print(data.loc[current_start])
            #     print(window_size_days)
            #     exit()

            predictions.append(np.average(current_predictions))
            errors.append(error)

        weights = np.array(1 - softmax(errors))
        predictions = np.array(predictions)
        # print(result)
        # result.append(np.dot(weights, predictions))
        result.append(predictions[0])

    # prices = data.loc[:,"bb:s5inft_index:px_last"]
    # prices = np.array(data.loc[:,"bb:s5inft_index:px_last"].dropna())
    # # prices = np.append(prices, result)

    # print(prices)
    # plt.plot(prices)
    # plt.plot(result)
    # plt.show()

    return result

    # TODO: store these results into the train -> predict folder so we can access the data when we use flags


# """
# Today is September 1 2018

# Black litterman is fed all data from Mar 1 2018 - September 1 2018

# Models are fed 6 mo. lagged data from Jan 1 2018 to March 1 2018 for training
# Models use data from March 1 2018 to September 1 2018 to predict price to March 1 2019

# Take the predicted time series from september 2 2018 to march 1 2019 and then took a moving average (lets say 1 week) for smoothing
# the value of the moving average of predicted price on march 1 becomes our price prediction for black litterman
# That gets turned into P and Q
# """
