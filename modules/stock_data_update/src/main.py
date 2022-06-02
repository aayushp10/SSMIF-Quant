#!/usr/bin/env python3
"""
Stock data update
"""

##################################
# for handling relative imports  #
# compatible with lambda runtime #
##################################
if __name__ != '__main__':
    import sys
    from pathlib import Path
    current_file = Path(__file__).resolve()
    root = next(elem for elem in current_file.parents
                if str(elem).endswith('/src'))
    sys.path.append(str(root))
#################################

from loguru import logger
from time import sleep
from datetime import datetime, timedelta
from ssmif_sdk.models.current_holdings import get_current_holdings
from ssmif_sdk.models.historical_holding_data import historical_holdings_database, build_model_historical_holding_data
from ssmif_sdk.models.utils import initialize_databases
from ssmif_sdk.utils.constants import DELISTED_TICKERS
from ssmif_sdk.utils.dividends import populate_dividends

NUM_ATTEMPTS: int = 5  # attempts before giving up
WAIT_TIME: int = 1  # seconds to wait before trying again


def main():
    """
    main entrypoint

    This runs in the morning to get yesterday's closing data.
    """
    initialize_databases()
    current_time = datetime.now()
    today = current_time.date()
    last_week = today - timedelta(days=7)
    for ticker in historical_holdings_database.get_tables():
        if ticker in DELISTED_TICKERS:
            continue
        for i in range(NUM_ATTEMPTS):
            try:
                build_model_historical_holding_data(
                    ticker, upsert=True, populate=True, start_date=last_week)
                break
            except Exception as err:
                logger.error(
                    f'trial {i + 1}: problem populating data for ticker {ticker}')
                sleep(WAIT_TIME)
        logger.info(f'got data for ticker {ticker}')

    num_dividends: int = 0
    for ticker in get_current_holdings():
        for i in range(NUM_ATTEMPTS):
            try:
                num_dividends += len(populate_dividends(ticker, start_date=last_week,
                                                        dividend_datetime=current_time + timedelta(seconds=num_dividends)))
                break
            except Exception as err:
                logger.exception(err)
                logger.error(
                    f'trial {i + 1}: problem getting dividend data for ticker {ticker}')
                sleep(WAIT_TIME)
        logger.info(f'got dividend data for ticker {ticker}')


def lambda_handler(_event, _context) -> str:
    """
    handler for aws lambda
    """
    main()
    return 'update success'


@logger.catch(reraise=True)
def run_main():
    """
    run main function for testing
    """
    main()


if __name__ == '__main__':
    run_main()
