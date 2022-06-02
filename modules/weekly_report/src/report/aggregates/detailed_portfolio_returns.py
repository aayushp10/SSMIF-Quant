#!/usr/bin/env python3
"""
Get the detailed portfolio returns data
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
from typing import List
from report.detailed_holding_returns import DetailedHoldingReturns
from report.aggregates.snapshots import AggregateSnapshots
from ssmif_sdk.aggregates.benchmark import AggregateBenchmark
from ssmif_sdk.models.utils import initialize_databases
from ssmif_sdk.utils.main import get_percent_change


class DeltailedPortfolioReturns:
    """
    detailed portfolio returns helper class
    """

    def __init__(self, aggregate_snapshots: AggregateSnapshots, aggregate_benchmark: AggregateBenchmark):
        logger.info('getting detailed portfolio returns')

        self.portfolio_returns: List[DetailedHoldingReturns] = [
            DetailedHoldingReturns(snapshot, aggregate_benchmark) for snapshot in aggregate_snapshots.snapshots]
        self.portfolio_returns.sort(key=lambda returns: returns.ticker)

        self.month_equity_return = get_percent_change(
            aggregate_snapshots.total_value_mtm, aggregate_snapshots.total_month_open)
        self.month_compare = self.month_equity_return - aggregate_benchmark.month_return

        self.year_equity_return = get_percent_change(
            aggregate_snapshots.total_value_mtm, aggregate_snapshots.total_year_open)
        self.year_compare = self.year_equity_return - aggregate_benchmark.year_return

        self.equity_life_return = get_percent_change(
            aggregate_snapshots.total_value_mtm, aggregate_snapshots.total_invested_amount)

    def __str__(self) -> str:
        """
        to string method
        """
        return f'num portfolio returns: {len(self.portfolio_returns)}, year compare: {self.year_compare}'

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
    aggregate_snapshots = AggregateSnapshots()
    aggregate_benchmark = AggregateBenchmark()
    portfolio_returns = DeltailedPortfolioReturns(
        aggregate_snapshots, aggregate_benchmark)
    logger.info(portfolio_returns)


if __name__ == '__main__':
    main()
