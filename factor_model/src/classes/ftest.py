import os
import pandas as pd


def get_data():
    filedir = os.path.abspath(
        r"SSMIF-Quant-Risk-Screen/flaskr/FactorModel/data/raw_data/test project")
    filename = "bb_s5finl_index.csv"
    filepath = os.path.join(filedir, filename)
    df = pd.read_csv(filepath)
    return df


def run_regression_for_sector(sector):
    factors = list(sector.columns)
    factors.remove('PX_LAST')
    factors.remove('date')

    sector_returns = sector['PX_LAST']
    # print(sector_returns)

    for factor in factors:
        factor_values = sector[factor]
        correlation = train_model(sector_returns, factor_values)
        # plot correlation


def get_sectors():
    # write code to get sectors
    return df of sectors(key sector name, value sector df)


def main():
    sectors = get_sectors()
    for sector in sectors:
        run_regression_for_sector(sector)


main()
