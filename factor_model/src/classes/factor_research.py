"""
file for factor research
"""

#from train.linear_regression import LinearRegression
#from train.base_model import BaseModel
# ^regression imports

# fix import yaml
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from clean.dataclean import CleanData
from classes.normalized_column import NormalizedColumn
from typing import Dict

from sklearn.compose import TransformedTargetRegressor


class FactorResearch():

    def __init__(self, sector_data: Dict[str, CleanData]):
        """
        once we have the cleaned bloomberg data in the main file, this can be run anytime after that
        we must pass in the sector_data and intitalize it here to get the data we need
        """
        self.sector_data = sector_data

        # sector.bloomberg_data.data[]

    # TODO: Aayush, remember to look into Canonical Correlation to see which factors can be used to maximize correlation to sector returns

    def run_factor_research(self):

        sector_correlations: Dict[str, pd.DataFrame] = {}

       # factor_returns: Dict[FactorType, float] = {}  #factor type

        returns: Dict[str, pd.DataFrame] = {}

        for sector_type, sector in self.sector_data.items():

            sector_price = sector.data[sector.target.normalize_colname()]
            sector_returns = sector_price.pct_change()[1:]
            factor_prices = sector.data.drop(
                sector.target.normalize_colname(), axis=1)
            factor_returns = factor_prices.pct_change()[1:]

            dataframes = [sector_returns, factor_returns]

            #returns[sector_type] = pd.concat(dataframes, axis=1)

            returns = pd.concat(dataframes, axis=1)
            correlation_matrix = returns.corr()
            sector_correlations[sector_type] = correlation_matrix[sector.target.normalize_colname(
            )]

            print("Factor Research")

       # exit()

            for col in factor_returns:

                model = LinearRegression()

                #factor_returns[col].fillna(factor_returns[col].mean(), inplace=True)

               # print(len(sector_returns), len(factor_returns[col]))

                X_train, X_test, y_train, y_test = train_test_split(
                    sector_returns, factor_returns[col], test_size=1/3, random_state=0)
                X_train = np.array(X_train).reshape(-1, 1)
                X_test = np.array(X_test).reshape(-1, 1)

                model.fit(X_train, y_train)

                #lr = TransformedTargetRegressor(model=model, func=np.log, inverse_func=np.exp)

                #lr.fit(X_train, y_train)

                y_pred = model.predict(X_test)

                print(
                    f"Your R^2 for factor: {col} in {sector_type} is : {r2_score(y_pred, y_test)}")

        print("Sector Correlations \n")

        print(sector_correlations)

        # ticker = list(self.sector_data[sector].bloomberg_data.keys())[0]

        #    # self.sector_data[sector].bloomberg_data[ticker].data[col.normalize_colname()].iloc[-1]

        #     #sector_dict = pd.to_dict(sector_returns.concat(factor_data))

        #     px_returns = pd.DataFrame.from_dict(list(self.sector_returns.keys(), ['PX_LAST'].values())) #df with px returns

        #     new_dict = px_returns.to_dict()

        #     for sector in sector.bloomberg_data.data[sector.target.normalized_column() != 'PX_LAST']:

       # pass
        # sector_df = pd.DataFrame(sector_returns.values(), columns = [sector_returns.keys()])

        # def run_regression(self):

        #

        """
        
        for the values of in each sector object that is in the sector_data dictionary
            calculate the returns of the sector px_last
            calculate the returns of each sector factor
            create a dictionary with the dataframe to each sector and its px_last returns and factor returns

        for each dataframe in dictionary of sectors
            for each factor in sector data that is not px_last
                run a linear regression to find the LINEAR correlation between their returns
                save this correlation to a dictionary of dictionaries
                - the outer dictionary is each sector and each sector has a dictionary with
                  keys and values. the keys are the factor and the values are the correlation
                  it has with the returns
                TODO: after linear version works, find other models to improve accuracy of the RF and ARIMA
                TODO: after this, run again based on the long and short optimization data points
        
        plot a heatmap depicting the correlation of each factor to each sector 
        - the correlation and name of each factor can be found as the key, value pair 
          inside the inner dictionary we saved earlier
        - the sector can be found by looking at the keys of the outer dictionary we saved earlier
        - for this heatmap, we have to use seaborn heat map
        - SAVE ALL PLOTS TO PDFS
        """

    def factor_returns(self):
        """
        TODO: for each different factor (momentum, value, quality...), use the data and put it together to find the return
        """

        pass

    # def factorResearch(global_config: GlobalConfigData, sector: Sector, clean_data: CleanData):

    # clean_data = CleanData(global_config.project, sector.sector, project.predict.bloomberg_data, project.predict.additional_data)
    # clean_data.extrapolate_to_date(sector.predict.output_window.end_date)
    # data = clean_data.data

    # TODO - the entire factor research


"""
inputs: 
    current factor dataframe
    returns of each sector

    1-year, 5-year ...


outputs:
    correlations of each factor to the returns of each sector

note:
    make the output for this a heatmap with the correlations so its easy for someone on the advisory board
    or someone like kaufman to just understand

    also, use the sklearn linear regression to do this


"""
