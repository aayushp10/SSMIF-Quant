#!/usr/bin/env python3
"""
hrp
"""
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
#################################
import yfinance as yf
from loguru import logger
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as pt
import scipy.cluster.hierarchy as sch

from os.path import join
from scipy.special import softmax

from typing import List, Optional
from constants import results_folder, hrp_weights_path

from utils.utils import relative_file_path


class HRP:
    """
    HRP with inspiration from https://medium.com/datadriveninvestor/hierarchical-risk-parity-in-portfolio-construction-fc368db18c78
    """

    def __init__(self, _, input_projects: List[str]):
        """
        Load the data from the project operated data
        """
        # TODO: make this better, it's a little bit of a hack
        hrp_key: str = "hrp"
        inputs_key: str = "inputs"
        data: List[pd.DataFrame] = []
        for tickername in input_projects.get(hrp_key, {}).get(inputs_key, {}):
            filepath = relative_file_path(
                f"{join(results_folder, tickername)}.csv")
            data.append(pd.read_csv(filepath))

        if len(data) <= 1:
            raise ValueError(
                "Must have more than one input to optimzie a portfoio")

        try:
            self.ticker_data = pd.concat(data)
        except Exception as err:
            logger.error(
                "unable to concat input dataframes, should be over the same time horizon and have one column")
            raise err

        self.weights = self.get_allocation_weights(self.ticker_data)
        self.weights.to_csv(hrp_weights_path, mode='a', header=False)

    @classmethod
    def get_allocation_weights(cls, ticker_data: pd.DataFrame):
        """
        input dataframe should have one column and T rows, the list length is denoted as N
        """
        # TODO: add error handling on the input
        data = ticker_data
        correlation_matrix = data.corr()
        covariance_matrix = data.cov()
        distance_matrix = HRP.get_distance_matrix(
            correlation_matrix, HRP.distance)
        # single denoted that clusters are determined by the minimum distance as in the original paper
        # TODO: single v ward depending on the situation, get linkage parameters exposed
        # scipy says this: The symmetric non-negative hollow observation matrix looks suspiciously like an uncondensed distance matrix
        link = sch.linkage(distance_matrix, 'single')

        # plot
        # dn = sch.dendrogram(link, labels=list(ticker_data.columns), leaf_rotation=90, distance_sort='descending',
        #                     count_sort='descendent')
        # pt.show()

        quasi_diag_matrix = HRP.get_quasi_diag_matrix(link)
        # this isnt quite correct, its doubling up on things instead of sorting them
        sort_corr = correlation_matrix.index[quasi_diag_matrix].tolist()

        raw_hrp_weights = HRP.get_recursive_bisection(
            covariance_matrix, sort_corr)
        normalized_hrp_weights = HRP.normalize_weights(
            0.05, 0.25, raw_hrp_weights, correlation_matrix)

        return normalized_hrp_weights

    @classmethod
    def normalize_weights(cls, minimum, maximum, raw_weights, correlation_matrix, blacklist=[]):
        """
        we have a min, max, the raw weights, and the correlations of all of the assets
        """
        indexes = list(correlation_matrix.index)

        # print(type(indexes.index()))
        raw_weights = sorted(list(map(lambda x: (x, raw_weights[x]), list(
            raw_weights.keys()))), key=lambda x: x[1])
        eps = .0005
        # # we assume that indexes[i] = the ith element in additions
        # print(depth_count)
        print(raw_weights)
        print(correlation_matrix)
        # exit()

        print(blacklist)
        for i, (tickername, weight) in enumerate(raw_weights):
            if(not tickername in blacklist):

                if weight > (maximum + eps):
                    print(f"REMOVING FROM: {tickername}")

                    _corr = correlation_matrix[tickername]
                    corr = list(map(lambda x: x if x != 1.0 else 0, _corr))
                    addition_weights = softmax(corr)
                    difference = weight - maximum
                    additions = difference * addition_weights
                    raw_weights[i] = (raw_weights[i][0], maximum)
                    raw_weights = pd.DataFrame(raw_weights).set_index(0)[
                        1]  # raw weights will be a series
                    normalized_weights = raw_weights.add(additions)
                    blacklist.append(tickername)
                    normalized_weights = cls.normalize_weights(
                        minimum, maximum, normalized_weights, correlation_matrix, blacklist=blacklist)

                    return normalized_weights

                elif weight < (minimum - eps):
                    print(f"ADDING TO: {tickername}")
                    _corr = correlation_matrix[tickername]
                    corr = list(map(lambda x: x if x != 1.0 else 0, _corr))
                    subtraction_weights = softmax(corr)
                    difference = minimum - weight
                    subtractions = difference * subtraction_weights
                    raw_weights[i] = (raw_weights[i][0], minimum)
                    raw_weights = pd.DataFrame(raw_weights).set_index(0)[
                        1]  # raw weights will be a series
                    normalized_weights = raw_weights.subtract(subtractions)
                    blacklist.append(tickername)
                    normalized_weights = cls.normalize_weights(
                        minimum, maximum, normalized_weights, correlation_matrix, blacklist=blacklist)

                    return normalized_weights

                else:
                    continue
            else:
                continue

        return pd.DataFrame(raw_weights).set_index(0)[1]

    @classmethod
    def getIVP(cls, cov):
        # Compute the inverse-variance portfolio
        ivp = 1. / np.diag(cov)
        ivp /= ivp.sum()
        return ivp

    @classmethod
    def getClusterVar(cls, cov, cItems):
        # Compute variance per cluster
        cov_ = cov.loc[cItems, cItems]  # matrix slice
        w_ = cls.getIVP(cov_).reshape(-1, 1)
        cVar = np.dot(np.dot(w_.T, cov_), w_)[0, 0]
        return cVar

    @classmethod
    def get_recursive_bisection(cls, cov, sort_corr):
        """
        Perform recursive bisection
        """
        # This is straight from https://medium.com/datadriveninvestor/hierarchical-risk-parity-in-portfolio-construction-fc368db18c78
        w = pd.Series(1, index=sort_corr)
        cItems = [sort_corr]  # initialize all items in one cluster
        while len(cItems) > 0:
            cItems = [i[j:k] for i in cItems for j, k in (
                (0, len(i) // 2), (len(i) // 2, len(i))) if len(i) > 1]  # bi-section
            for i in range(0, len(cItems), 2):  # parse in pairs
                cItems0 = cItems[i]  # cluster 1
                cItems1 = cItems[i + 1]  # cluster 2
                cVar0 = cls.getClusterVar(cov, cItems0)
                cVar1 = cls.getClusterVar(cov, cItems1)
                alpha = 1 - cVar0 / (cVar0 + cVar1)
                w[cItems0] *= alpha  # weight 1
                w[cItems1] *= 1 - alpha  # weight 2
        return w

    @classmethod
    def get_quasi_diag_matrix(cls, link):
        """
        get a quasi diagonal matrix
        """
        # TODO: parameterize  https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.fcluster.html#scipy.cluster.hierarchy.fcluster
        # TODO: checkout fcluster
        # TODO: check replacing the linkage and this step with a single fclusterdata call
        # sp = sch.fcluster(link, 0.3, criterion='distance')
        # print("sp is", sp)
        # Sort clustered items by distance
        # This is straight from https://medium.com/datadriveninvestor/hierarchical-risk-parity-in-portfolio-construction-fc368db18c78
        link = link.astype(int)
        sortIx = pd.Series([link[-1, 0], link[-1, 1]])
        numItems = link[-1, 3]  # number of original items
        while sortIx.max() >= numItems:
            sortIx.index = range(0, sortIx.shape[0] * 2, 2)  # make space
            df0 = sortIx[sortIx >= numItems]  # find clusters
            i = df0.index
            j = df0.values - numItems
            sortIx[i] = link[j, 0]  # item 1
            df0 = pd.Series(link[j, 1], index=i + 1)
            sortIx = sortIx.append(df0)  # item 2
            sortIx = sortIx.sort_index()  # re-sort
            sortIx.index = range(sortIx.shape[0])  # re-index
        return sortIx.tolist()
        # return sp

    @staticmethod
    def distance(matrix):
        """
        sqrt((1/2) * (1-matrix)) - this is the original distance equation from MLP's hrp paper
        """
        return ((1-matrix)/2.)**.5

    @classmethod
    def get_distance_matrix(cls, correlation_matrix, dist_func):
        return dist_func(correlation_matrix)


if __name__ == "__main__":
    # tickers = ["CSJ", "TIP", "IEF", "TLT", "LQD", "BND", "XLU", "XLE", "XLF", "FXI", "XLB", "EEM", "XLK", "SPY", "DIA", "EPP", "EWU", "EWG", "EWQ", "EFA", "VGK", "EWJ", "VPL"]
    tickers = ["XLK", "XLF", "XLE", "XLV",
               "XLP", "XLY", "XLI", "XLU", "XLC", "XLB"]
    data = []
    for ticker in tickers:
        data.append(yf.download(ticker, start='2018-01-01',
                    end='2020-11-16')['Adj Close'])
    # data: pd.DataFrame = yf.download('msft aapl goog tsla ba dis zm twtr', start='2018-01-01', end='2020-01-01')
    for i in range(len(data)):
        data[i] = data[i].rename(tickers[i])
    # data is an TxN matrix   503x23
    stock_prices = pd.DataFrame(data).T
    print(stock_prices)
    # HRP = HRP(stock_prices)
