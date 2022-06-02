#!/usr/bin/env python3
"""
Get the capital gains for the portfolio
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
from ssmif_sdk.utils.enums import StockTransactionType
from ssmif_sdk.models.company_data import get_company_data
from ssmif_sdk.models.utils import initialize_databases
from ssmif_sdk.models.transactions import Stock_Transactions


class CapitalGains:
    """
    capital gains object
    """

    def __init__(self, ticker: str, company: str, purchase_date: date, sell_date: date,
                 shares: int, entry_price: float, sell_price: float):
        self.ticker = ticker
        self.company = company
        self.purchase_date = purchase_date
        self.sell_date = sell_date
        self.shares = shares
        self.entry_price = entry_price
        self.invested_value = self.entry_price * self.shares
        self.sell_price = sell_price
        self.sell_value = self.sell_price * self.shares
        self.capital_gains = self.sell_value - self.invested_value


class CapitalGainsData:
    """
    Capital Gains helper class
    """

    def __init__(self, today: Optional[date] = None) -> None:
        if today is None:
            today = date.today()
        year_start, _ = get_year_month_start(today)
        transactions_data = Stock_Transactions.select().where(
            (Stock_Transactions.date >= year_start) &
            (Stock_Transactions.type == StockTransactionType.sell))
        self.capital_gains: List[List[CapitalGains]] = [[]
                                                        for _ in range(today.month)]
        self.sums: List[float] = [0.] * today.month
        self.year_total: float = 0.
        self.month_open: float = 0.

        stored_company_data: Dict[str, str] = {}
        for current_data in transactions_data:
            ticker: str = current_data.ticker
            if ticker not in stored_company_data:
                stored_company_data[current_data.ticker] = get_company_data(
                    ticker).name
            company_name = stored_company_data[ticker]
            current_datetime: datetime = current_data.date
            capital_gains_object = CapitalGains(
                ticker, company_name, current_data.purchase_date, current_data.date,
                current_data.shares, current_data.entry_vwap, current_data.sale_vwap)
            amount = capital_gains_object.capital_gains
            self.capital_gains[current_datetime.month -
                               1].append(capital_gains_object)
            self.sums[current_datetime.month - 1] += amount
            self.year_total += amount
            if current_datetime.month < today.month:
                self.month_open += amount

    def __str__(self) -> str:
        """
        to string method
        """
        return f'{len(self.capital_gains)} month(s), total {self.year_total}'

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
    initialize_databases()
    capital_gains = CapitalGainsData()
    logger.info(capital_gains)


if __name__ == '__main__':
    main()
