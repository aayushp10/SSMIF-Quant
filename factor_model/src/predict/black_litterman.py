#!/usr/bin/env python3
"""
black litterman
"""
from __future__ import annotations
#################################
# for handling relative imports #
#################################
if __name__ == '__main__':
    import sys
    from pathlib import Path
    current_file = Path(__file__).resolve()
    root = next(elem for elem in current_file.parents
                if str(elem).endswith('src'))
    sys.path.append(str(root))
    # remove the current file's directory from sys.path
    try:
        sys.path.remove(str(current_file.parent))
    except ValueError:  # Already removed
        pass

from pypfopt import black_litterman
from pypfopt.black_litterman import BlackLittermanModel
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import black_litterman
from predict.optimizer import Optimizer
from utils.enums import OptimizerType, SectorType, DataSource
from predict.prediction_data import Prediction
from clean.dataclean import CleanData
import pandas as pd
import numpy as np
import yfinance as yf
from typing import Dict, List, Tuple
from classes.bloomberg import BloombergData
from classes.sector import Sector
from classes.normalized_column import NormalizedColumn
from predict.hrp import HRP
from scipy.special import softmax
from loguru import logger


class BlackLitterman(Optimizer):
    weights: Dict[SectorType, float] = []
    optimizer_type = OptimizerType.black_litterman

    def __init__(self, predictions: List[Prediction],
                 hyperparameters: Dict[str, Any],
                 market_cap_weights: Dict[SectorType, float],
                 benchmark: Dict[str, Any]):
        super().__init__(hyperparameters, benchmark)
        self.predictions = predictions
        self.market_cap_weights = market_cap_weights

    def run_optimization(self, predictions: Dict[SectorType, List[float]], sector_data: Dict[SectorType, Tuple[CleanData, NormalizedColumn]]) -> None:
        """
        run optimization logic
        """

        # Find the covariance matrix of the daily returns dataframe for each sector
        daily_returns = pd.DataFrame(predictions).pct_change()
        daily_returns.dropna(inplace=True)

        cov = daily_returns.cov()

        # p = [[0 for sector in prediction.keys()] for sector in prediction.keys()]
        q = []
        n = len(predictions.keys())
        p = np.zeros((n, n), dtype=float)
        i = 0
        mcaps = {}
        # es = pd.DataFrame({'Sector': list(ro.r("sectorNames")),
    #                             'Linear Regression': list(ro.r("accuracyMatrix[1, ]")),
    #                             'ARIMA Analysis': list(ro.r("accuracyMatrix[2, ]")),
    #                             'Random Forest': list(ro.r("accuracyMatrix[3, ]"))}).set_index("Sector").T
        corr_returns_dict = {}

        for sector, values in predictions.items():
            values = daily_returns[sector]
            cum_sum = 1
            for index, value in values.iteritems():
                cum_sum *= (1+value)
            predicted_return = cum_sum - 1
            p_val = 1
            if predicted_return < 0:
                p_val = -1
                predicted_return *= -1
            q.append(predicted_return)
            p[i][i] = p_val
            i += 1

            current_clean_sector_data, current_target = sector_data[sector]
            ticker = NormalizedColumn.from_str(
                list(current_clean_sector_data.data.keys())[0]).name

            col = NormalizedColumn(DataSource.bloomberg, ticker, "CUR_MKT_CAP")
            mcaps[sector] = current_clean_sector_data.data[col.normalize_colname()
                                                           ].iloc[-1]

            corr_returns_dict[sector] = current_clean_sector_data.data[current_target.normalize_colname()]

        corr_returns = pd.DataFrame(
            corr_returns_dict).pct_change().dropna(inplace=False)
        corr_matrix = corr_returns.corr()

        q = np.array(q).reshape(-1, 1)

        weights = {}
        for ticker, bbg in self.benchmark.items():
            market_returns = bbg.data["PX_LAST"]
            delta = black_litterman.market_implied_risk_aversion(
                market_returns)

            # Prior returns which are generated by using the market caps, delta and covariance matrix
            prior = black_litterman.prior = black_litterman.market_implied_prior_returns(
                mcaps, delta, cov)

            # Create a Black Litterman object
            bl = BlackLittermanModel(cov, pi=prior, P=p, Q=q)

            # Use the delta to find the optimal allocation weights and then return the final cleaned weights
            bl.bl_weights(delta)

            weights[ticker] = bl.clean_weights()

            weights_array = sorted(list(map(lambda x: (x, weights[ticker][x]), list(
                weights[ticker].keys()))), key=lambda x: x[1])
            weights_only = list(map(lambda x: x[1], weights_array))
            sectors_only = list(map(lambda x: x[0], weights_array))
            real_weights = softmax(weights_only)
            for i in range(len(real_weights)):
                weights[ticker][sectors_only[i]] = real_weights[i]

        self.weights = weights

    @classmethod
    def from_dict(cls, input_dict: Dict[str, Any]) -> BlackLitterman:
        """
        constructor for model object from dict
        """
        predictions_key: str = 'predictions'
        hyperparameters_key = 'hyperparams'
        market_cap_weights_key: str = 'market_cap_weights'
        benchmark_key: str = 'benchmark'
        sector_data_key: str = 'sector_data'

        predictions: List[Prediction] = []
        for raw_prediction_config in input_dict[predictions_key]:
            predictions.append(Prediction.from_dict(raw_prediction_config))

        hyperparameters: Dict[str, Any] = input_dict[hyperparameters_key]

        market_cap_weights: Dict[SectorType, float] = {}
        for sector_type, market_cap_weight in input_dict[market_cap_weights_key].items():
            if not SectorType.has_value(sector_type):
                raise ValueError(f'invalid sector type {sector_type} provided')
            sector_type_obj = SectorType(sector_type)
            market_cap_weights[sector_type_obj] = market_cap_weight

        return cls(predictions, hyperparameters, market_cap_weights, input_dict[benchmark_key])

    def scale_weights(self, weights: Dict[SectorType, float]) -> Dict[SectorType, float]:
        """
        function that scales the weights of the allocations between a given constraint
        """

        w = weights.values()
        curr_min_weight = min(w)
        curr_max_weight = max(w)

        new_max = .25
        new_min = .05

        new_weights: Dict[SectorType, float] = {}
        for sector_type, weight in weights.items():
            new_weights[sector_type] = (((weight - curr_min_weight) * (
                new_max - new_min)) / (curr_max_weight - curr_min_weight)) + new_min

        return new_weights

# if __name__ == '__main__':
#     daily_returns = pd.read_csv('Returns.csv')
#     spy = pd.read_csv("spy.csv")["Adj Close"]
#     black_litterman = BlackLitterman(daily_returns, spy)