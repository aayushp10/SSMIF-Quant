"""
    An optimization algorithm to generate portfolio weights based off of our price projections
    Theoretical: HRP (hierarchical Risk Parity)
"""

"""
    TREE CLUSTERING 

    TxN matrix of observations X : N variables over T periods

    ex: 5 x 3
    Price   P/E     P/B
1   100     7        ...
2   101     6.9
3   100.5   7.1
4   99      6.95
5   105     7


compute NxN correlation matrix with entries p = {p_i_j}_i_j=1...N
p_i_j = [X_i, X_j]


3 x 3 Correlation Matrix

        Price    P/E     P/B
Price    1       #       #

P/E      #       1       #
 
P/B      #       #       1

define distance measure d(A, B) E [0, 1] = sqrt(0.5*(1-p_i_j))
        Price    P/E     P/B
Price    f(1)    #       #

P/E      f(#)    1       #
 
P/B      #       #       1

This lets us compute an NxN distance matrix D 


"""




import pandas as pd
import numpy as np
from typing import List
from loguru import logger
from os.path import join
from model_utils import get_file_list
from error_handling import HandleErrors
from constants import clean_data_folder
def _calculate_distance(x):
    return np.sqrt(0.5*(1-x))


def calculate_distance_matrix(frame: pd.DataFrame) -> np.ndarray:
    """
        Calculate and return the distance matrix of the given data frame based off of the following formula laid out by Lopez de Prado
        dist = sqrt(0.5 * (1-x)) for every x in the correlation matrix of a dataframe
        https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2708678

    """
    frame = frame.drop(columns=['date', 'PX_LAST'])
    # Compute the correlation matrix  (also a pandas built in)
    corrMatrix = frame.corr()
    # compute distance matrix
    dist_matrix = corrMatrix.applymap(_calculate_distance)

    return np.asarray(dist_matrix)


def calculate_d_bar(dist_matrix: np.ndarray) -> np.ndarray:
    """
    Calculate Dbar for the input distance matrix. A quick explanation regarding the difference between D and Dbar
     – for two assets i and j, D(i,j) is the distance between the two assets while Dbar(i,j) indicates the closeness in similarity of these assets with the rest of the portfolio. 
     This becomes apparent when we look at the formula for calculating Dbar – we sum over the squared difference of distances of i and j from the other stocks. 
     Hence, a lower value means that assets i and j are similarly correlated with the other stocks in our portfolio.
    """
    dbar: np.ndarray = np.zeros(dist_matrix.shape)
    for i in range(dist_matrix.shape[0]):
        for j in range(dist_matrix.shape[1]):
            # dbar i, j is the pairwise euclidean distance of the rows in columns i and j summed up
            temp = dist_matrix[:, i] - dist_matrix[:, j]
            temp = temp*temp
            dbar[i, j] = np.sqrt(temp.sum())

    return dbar


@HandleErrors
def main():
    glob_rel_path: str = join(clean_data_folder, "sentiment*.csv")
    paths: List[str] = get_file_list(glob_rel_path, name="foo")
    logger.info(paths)
    for filepath in paths:
        df: pd.DataFrame = pd.read_csv(filepath)
        dist_matrix = calculate_distance_matrix(df)
        dbar = calculate_d_bar(dist_matrix)

    # return


if __name__ == "__main__":
    main()
