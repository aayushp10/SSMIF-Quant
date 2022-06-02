import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from datetime import datetime
from loguru import logger
from clean.dataclean import CleanData


class RegimeModel():

    def __init__(self, benchmarkData: CleanData):
        # print(type(benchmarkData.data))
        # exit()
        self.benchmarkData = benchmarkData.data
        self.threshold = 0.15
        # self.benchmarkData = pd.Series(benchmarkData.data)
        # self.benchmarkData = benchmarkData[list(benchmarkData.keys())[0]]

    def highVolatilityProbabilities(self):

        # Read in the asset data and resample it
        assetReturns = self.benchmarkData.resample(
            "W").last().pct_change().dropna()

        # Create a regime model using a Markov Regression with 3 regimes (low, medium, high) and use the variance to determine the regimes
        logger.info("\nInitiating Regime Switching Markov Regression\n")
        regimeModel = sm.tsa.MarkovRegression(
            assetReturns, k_regimes=3, switching_variance=True)
        regimeResiduals = regimeModel.fit()

        # Store the probabilities for having a high volatility regime
        self.highVolatilityRegime = regimeResiduals.smoothed_marginal_probabilities[2]

        logger.success(
            f"Here are the high volatility regime statistics: {regimeResiduals.summary()}")
        logger.success(
            f"The expected duration of a high volatility regime is {regimeResiduals.expected_durations[2]}")

        return self.highVolatilityRegime

    def find_periods_of_high_vol(self):
        pass

    def is_high_vol_regime(self):
        if (self.highVolatilityRegime[-1] < self.threshold):
            return False
        return True

    def visualize_regimes(self):

        plt.plot(self.highVolatilityRegime)
        plt.savefig("visualizations/High-Volatility-Regime-Probabilities.png")


'''
Short Model requires regimes to be recalculated every 6 months so must run along with the model
Long Model we can cache the past 6 years of data and use those long term training periods 
'''
