#!/usr/bin/env python3
"""
Get the asset allocation for the portfolio,
compare to benchmark (s&p)
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
from typing import List, Optional
from ssmif_sdk.models.current_holdings import get_shares_amount
from ssmif_sdk.models.utils import initialize_databases
from ssmif_sdk.models.sector_allocations import Sector_Allocations
from ssmif_sdk.utils.enums import SectorType, sector_etfs
from ssmif_sdk.utils.stock_price import get_stock_price
from ssmif_sdk.utils.sector_allocations import get_portfolio_allocations
from ssmif_sdk.utils.constants import BENCHMARK_PURCHASED_TICKER


class Allocation:
    """
    sector weights comparison object
    """

    def __init__(self, sector: SectorType, ticker: str, portfolio_weight: float, factor_model_weight: float,
                 benchmark_weight: float, benchmark_value: float, holdings_value: float):
        self.sector = sector
        self.sector_ticker = ticker
        self.portfolio_weight = portfolio_weight
        self.factor_model_weight = factor_model_weight
        self.benchmark_weight = benchmark_weight
        self.portfolio_factor_model_difference = self.portfolio_weight - \
            self.factor_model_weight
        self.portfolio_factor_model_underweight = self.portfolio_factor_model_difference < 0
        self.benchmark_value = benchmark_value
        self.holdings_value = holdings_value
        self.total = self.benchmark_value + self.holdings_value
        self.portfolio_benchmark_difference = self.portfolio_weight - \
            self.factor_model_weight
        self.portfolio_benchmark_underweight = self.portfolio_benchmark_difference < 0


class AssetAllocation:
    """
    Asset Allocation helper class
    """

    def __init__(self, total_portfolio_value: Optional[float] = None) -> None:

        benchmark_shares, _ = get_shares_amount(BENCHMARK_PURCHASED_TICKER)
        benchmark_stock_price = list(get_stock_price(
            BENCHMARK_PURCHASED_TICKER).values())[0][0]
        total_benchmark_position = benchmark_shares * benchmark_stock_price

        portfolio_allocations = get_portfolio_allocations(
            total_portfolio_value - total_benchmark_position)

        self.total_portfolio_weights = 0.
        self.total_benchmark_weights = 0.
        self.allocations: List[Allocation] = []

        for allocation in Sector_Allocations.select():
            sector: SectorType = allocation.sector
            ticker = sector_etfs[allocation.sector]
            benchmark_value = total_benchmark_position * allocation.benchmark
            allocation_object = Allocation(sector, ticker, portfolio_allocations.weights[sector],
                                           allocation.factor_model, allocation.benchmark,
                                           benchmark_value, portfolio_allocations.values[sector])
            self.allocations.append(allocation_object)
            self.total_portfolio_weights += allocation_object.portfolio_weight
            self.total_benchmark_weights += allocation.benchmark

    def __str__(self) -> str:
        return f'{len(self.allocations)} allocations. total portfolio weights: {self.total_portfolio_weights:.2f}' + \
            f', total benchmark weights: {self.total_benchmark_weights:.2f}'

    def __repr__(self) -> str:
        return str(self)


@logger.catch(reraise=True)
def main():
    """
    main function for testing
    """
    initialize_databases()
    asset_allocations = AssetAllocation()
    logger.info(asset_allocations)


if __name__ == '__main__':
    main()
