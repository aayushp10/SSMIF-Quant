"""
class for backtesting using the zipline library
"""


#################################
# for handling relative imports #
#################################
if __name__ == '__main__':
    import sys
    from pathlib import Path
    current_file = Path(__file__).resolve()
    root = next(elem for elem in current_file.parents
                if str(elem).endswith('/src'))
    sys.path.append(str(root))
    try:
        sys.path.remove(str(current_file.parent))
    except ValueError:  # Already removed
        pass
#################################


from utils.enums import SectorType
from predict.prediction_data import Prediction
from clean.dataclean import CleanData
from classes.global_config_data import GlobalConfigData
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List

from collections import Counter
import matplotlib.pyplot as plt
from loguru import logger
from datetime import datetime, timedelta


class Backtest:

    def __init__(self, global_config: GlobalConfigData, sector_data: Dict[SectorType, CleanData], weights: Dict[SectorType, float], benchmark_data):
        '''self.weights = {'tech': 0.22, 'hlth': 0.18, 'cond': 0.15, 'tels': .13,
            'fin': .16, 'indu': .07, 'cons': .12, 'util': .11, 'matr': .05, 'eng': .10}'''
        # print(sector_data)
        self.sector_data = sector_data
        self.weights = weights
        self.benchmark_data = benchmark_data[list(benchmark_data.keys())[0]]
        self.window = global_config.window

        # for bloomberg prices, it's always "PX_LAST"

    # def addMonths(self):

    def custom_cumulative_return_calc(self, returns, starting_value=1):
        l = []
        last = starting_value
        for r in returns:
            c = last*r
            l.append(c)
            last = c
        return l

    def run_backtest_on_df(self, weights: pd.DataFrame):
        '''
        run backtest with given dataframe
        '''
        weights.to_csv("outputs/weights.csv")
        logger.info(f"weights: {weights}")
        logger.info(f"weights keys: {list(weights.keys())}")
        benchmark_key = 'benchmark'

        daily_returns_of_sectors = {}
        for sector, sd in self.sector_data.items():
            daily_returns_of_sectors[sector] = sd.data[sd.target.normalize_colname(
            )].pct_change()

        daily_returns_of_benchmark = self.benchmark_data.data["PX_LAST"].pct_change(
        )

        returns_based_on_weights: Dict[SectorType, List[float]] = {}
        benchmark_returns = []
        for date, row in weights.iterrows():
            for sector, sd in self.sector_data.items():
                if sector not in returns_based_on_weights:
                    returns_based_on_weights[sector] = []
                returns_based_on_weights[sector].append(
                    daily_returns_of_sectors[sector].loc[date] * row[sector])

            benchmark_returns.append(daily_returns_of_benchmark.loc[date])

        port_returns = pd.Series([])
        for sector, returns in returns_based_on_weights.items():
            if len(port_returns) == 0:
                port_returns = pd.Series(returns)
            else:
                port_returns = np.add(port_returns, returns)

        port_cumulative_returns = (1 + pd.Series(port_returns)).cumprod()
        benchmark_cumulative_returns = (
            1 + pd.Series(benchmark_returns)).cumprod()

        return port_cumulative_returns, benchmark_cumulative_returns

    def run_backtest(self, starting_cumulative_of_port=1.0, starting_cumulative_of_benchmark=1.0):

        sector_returns: Dict[SectorType, float] = {}
        sector_differences: Dict[SectorType, float] = {}

        startDate = '2020-08-01'
        spy_returns = self.benchmark_data.data["PX_LAST"].loc[startDate:]
        spy_returns = spy_returns.pct_change()

        spy_returns.dropna(inplace=True)

        # Gets daily returns for all sectors and stores in dictionary
        for sector, sd in self.sector_data.items():
            prices = sd.data[sd.target.normalize_colname()].loc[startDate:]

            returns = prices.pct_change()
            returns.dropna(inplace=True)
            z = {}
            print(self.weights['SPX Index'])
            z[sector] = returns*self.weights['SPX Index'][sector]
            sector_returns.update(z)

        bl_returns = sector_returns

        # Calculates black litterman returns by multiplying sector returns by test weights (FIX)
        # for sector in list(sector_returns.keys()):
        #     bl_returns[sector] = bl_returns[sector]*weights[sector]
        # bl_returns = {updated_returns: weights * sector_returns[updated_returns] for
        # updated_returns, weights in self.weights.items()}

        # Computes difference between sector daily returns and litterman returns and stores in dict
        # for key, returns in sector_returns.items():
        #     sector_differences[key] = returns - bl_returns.get(key)

        # Computes sum of bl returns and copmares to spy returns
        # total_bl_returns = sum(bl_returns.values())
        # total_spy_returns = sum(spy_returns.values())
        # return_difference = total_spy_returns-total_bl_returns

        # #Compute BL and SPY Volatility
        # bl_volatility = np.std(bl_returns.values()) * (252**0.5)
        # spy_volatility = spy_returns.std() * (252**0.5)
        # sector_volatility =  np.std(sector_returns.values()) * (252**0.5)

        # Table showing spy and bl returns and the difference between them
        # returns_table = {'SPY Sector Return': sector_returns, 'BL Sector Return': bl_returns, 'Return Difference': return_difference}
        # for row in zip(*([key] + (value) for key, value in sorted(returns_table.items()))):
        #     print(*row)

        port_returns = pd.Series([])
        for sector, returns in sector_returns.items():
            if len(port_returns) == 0:
                port_returns = pd.Series(returns)
            else:
                port_returns = np.add(port_returns, returns)

        # Get lists of rturns
        # bl_returns_list = list(bl_returns)
        sector_returns_list = list(sector_returns)
        spy_returns_list = spy_returns.values.tolist()

        # Calculate cumulatitve returns to use for graph

        bl_cumlative_returns = self.custom_cumulative_return_calc(
            (1 + port_returns), starting_cumulative_of_port)

        spy_cumulative_returns_list = self.custom_cumulative_return_calc(
            (spy_returns + 1), starting_cumulative_of_benchmark)

        #spy_cumulative_returns = ((spy_returns.iloc[-1] - spy_returns.iloc[0]) / spy_returns.iloc[0]) * 100

        # Plot spy returns vs. bl returns
        # logger.success(f"SSMIF Outperformed SP 500 by {bl_cumlative_returns.iloc[-1]-spy_cumulative_returns.iloc[-1]}")
        plt.plot(bl_cumlative_returns, color="green",
                 label="Factor Model Returns")
        plt.plot(spy_cumulative_returns_list,
                 color="black", label="S&P 500 Returns")
        plt.title("Factor Model Returns vs. S&P 500 Returns")
        plt.legend()
        plt.ylabel('Cumulative Returns')
        plt.savefig("visualizations/Backtest-Fig-Labeled.png")

        return bl_cumlative_returns, spy_cumulative_returns_list

        """
        this is what should output something
        """


"""
inputs:
    daily returns of each sector
    daily returns of the s&p 500
    black litterman asset allocation

calculations:
    calculate return of black litterman allocation
        note: have the allocation be refreshed at the end of every semester (january and june)
            this will be our "rebalance" that we do at the end of the semester and it can take
            into account any changes the model is predicting

backtest:
    compare the return of each BL sector allocation to each individual sector
    compare the return of the overall allocation to the S&P 500
        note: try to also keep a running metric for volatility during the backtest

output:
    graphical interpretations saved to disk of our sector comparison and S&P comparison
    graphical interpretation of our volatilities vs the sector and S&P volatilities
    our allocation performance vs the other comparision performance

note: 
    remember to keep this dynamic so that we can pass in allocations from anything and it isn't
    just relying on it to be black litterman allocations. this way we can test more things if we 
    decide to do so. for example, we can test a hierarchal risk parity allocation or even a manual
    allocation if we really want to

    refresh allocations every 6 months into the backtest
"""
