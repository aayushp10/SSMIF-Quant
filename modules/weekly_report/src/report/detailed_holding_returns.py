#!/usr/bin/env python3
"""
Get detailed holding returns for a given ticker
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

from loguru import logger
from ssmif_sdk.aggregates.benchmark import AggregateBenchmark
from ssmif_sdk.utils.main import get_percent_change
from ssmif_sdk.utils.stock_price import get_benchmark_price
from ssmif_sdk.models.utils import initialize_databases
from ssmif_sdk.models.current_holdings import get_current_holdings
from ssmif_sdk.compute.snapshot import Snapshot


class DetailedHoldingReturns:
    """
    detailed holding returns helper class
    """

    def __init__(self, snapshot: Snapshot, aggregate_benchmark: AggregateBenchmark):
        self.ticker = snapshot.ticker
        self.company = snapshot.company
        self.sector = snapshot.sector
        self.date = snapshot.date

        self.month_equity_return = get_percent_change(snapshot.current_value_mtm,
                                                      snapshot.month_open_value)
        self.month_compare = self.month_equity_return - aggregate_benchmark.month_return

        self.year_equity_return = get_percent_change(snapshot.current_value_mtm,
                                                     snapshot.year_open_value)
        self.year_compare = self.year_equity_return - aggregate_benchmark.year_return

        benchmark_price_original_purchase = list(
            get_benchmark_price(dates={self.date}).values())[0][0]
        self.benchmark_life_return = get_percent_change(aggregate_benchmark.current,
                                                        benchmark_price_original_purchase)
        self.life_equity_return = 1. if snapshot.invested_amount == 0. else \
            get_percent_change(snapshot.current_value_mtm,
                               snapshot.invested_amount)
        self.life_compare = self.life_equity_return - self.benchmark_life_return

    def __str__(self) -> str:
        """
        to string method
        """
        return f'detailed holdings returns of {self.ticker}: {self.life_equity_return} vs {self.benchmark_life_return}'

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
    current_holdings = get_current_holdings()
    snapshot = Snapshot(current_holdings[0])
    aggregate_benchmark = AggregateBenchmark(snapshot.today)
    holding_returns = DetailedHoldingReturns(snapshot, aggregate_benchmark)
    logger.info(holding_returns)


if __name__ == '__main__':
    main()
