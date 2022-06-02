import pandas as pd
import pandas_datareader as web
import numpy as np
import os
from os.path import join, basename, splitext
import datetime as dt
from sklearn.linear_model import LinearRegression
from data_visualization import get_csv_paths


def get_ticker_close(ticker):
    start_date = '2019-01-31'
    end_date = '2019-12-31'
    ticker_df = web.DataReader(ticker, 'yahoo', start=start_date, end=end_date)
    return ticker_df['Adj Close']


def get_data_array():

    file_paths_list = get_csv_paths()

    for file_path in file_paths_list:
        if basename(splitext(file_path)[0]).startswith("research_cpi_yoy_index"):
            df = pd.read_csv(file_path)
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date')
            data_array = np.array(df['PX_LAST']).reshape(-1, 1)
            return data_array


def linear_regression(ticker):

    x = get_data_array()

    closing_prices = get_ticker_close(ticker)
    y = np.array(closing_prices)

    model = LinearRegression().fit(x, y)
    r_squared = model.score(x, y)
    print(f"R-Squared = {r_squared}")


def main():
    ticker = 'SPY'
    return linear_regression(ticker)


if __name__ == "__main__":
    main()
