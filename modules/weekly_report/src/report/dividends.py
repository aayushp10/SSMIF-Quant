#!/usr/bin/env python3
"""
Get the dividends for the portfolio
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
    # remove the current file's directory from sys.path
    try:
        sys.path.remove(str(current_file.parent))
    except ValueError:  # Already removed
        pass
#################################

from datetime import date, datetime
from loguru import logger
from typing import List, Dict, Optional
from ssmif_sdk.utils.main import get_year_month_start
from ssmif_sdk.utils.enums import CashDepositType
from ssmif_sdk.models.company_data import get_company_data
from ssmif_sdk.models.utils import initialize_databases
from ssmif_sdk.models.transactions import Cash_Deposits


class Dividend:
    """
    dividend object
    """

    def __init__(self, ticker: str, company: str, allocation_date: date, amount: float):
        self.ticker = ticker
        self.company = company
        self.allocation_date = allocation_date
        self.amount = amount


class DividendsData:
    """
    dividends helper class

    note this uses current holdings only (no historical data)
    """

    def __init__(self, today: Optional[date] = None) -> None:
        if today is None:
            today = date.today()
        year_start, _ = get_year_month_start(today)
        dividend_data = Cash_Deposits.select(Cash_Deposits.ticker, Cash_Deposits.date, Cash_Deposits.amount).where(
            (Cash_Deposits.date >= year_start) & (Cash_Deposits.type == CashDepositType.dividend))
        self.dividends: List[List[Dividend]] = [[] for _ in range(today.month)]
        self.sums: List[float] = [0.] * today.month
        self.year_total: float = 0.
        self.month_open: float = 0.

        stored_company_data: Dict[str, str] = {}
        for current_data in dividend_data:
            ticker: str = current_data.ticker
            if ticker not in stored_company_data:
                stored_company_data[current_data.ticker] = get_company_data(
                    ticker).name
            company_name = stored_company_data[ticker]
            current_datetime: datetime = current_data.date
            amount = current_data.amount
            self.dividends[current_datetime.month - 1].append(Dividend(
                ticker, company_name, current_datetime.date(), amount))
            self.sums[current_datetime.month - 1] += amount
            self.year_total += amount
            if current_datetime.month < today.month:
                self.month_open += amount

    def __str__(self) -> str:
        """
        to string method
        """
        return f'{len(self.dividends)} month(s), total {self.year_total}'

    def __repr__(self) -> str:
        """
        return tostring representation
        """
        return str(self)


@logger.catch(reraise=True)
def main():
    """
    main function for testing
    """
    initialize_databases(clear_dividends=False)
    dividends = DividendsData()
    logger.info(dividends)


if __name__ == '__main__':
    main()
