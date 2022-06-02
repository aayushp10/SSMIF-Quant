#!/usr/bin/env python3
"""
Build excel report
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
from datetime import date
from report.excel.sheet_1 import BuildFirstSheet
from report.excel.sheet_2 import BuildSecondSheet
from report.excel.sheet_3 import BuildThirdSheet
from report.excel.sheet_4 import BuildFourthSheet
from report.excel.sheet_5 import BuildFifthSheet
from report.dividends import DividendsData
from report.capital_gains import CapitalGainsData
from report.aggregates.snapshots import AggregateSnapshots

from ssmif_sdk.aggregates.cash import AggregateCash
from ssmif_sdk.aggregates.benchmark import AggregateBenchmark
from ssmif_sdk.aggregates.stocks import AggregateStocks
from ssmif_sdk.aggregates.summary import Summary
from ssmif_sdk.misc.report_file_path import get_file_path
from ssmif_sdk.models.utils import initialize_databases
from ssmif_sdk.utils.constants import DEFAULT_PREVIOUS_REPORT_DELTA
from ssmif_sdk.utils.excel_builder import ExcelBuilder


class BuildExcel:
    """
    build excel class
    """

    def __init__(self, today: date = date.today()) -> None:
        previous_report_delta = DEFAULT_PREVIOUS_REPORT_DELTA

        previous_report = today - previous_report_delta

        self.today = today
        self.builder = ExcelBuilder(get_file_path(self.today))

        dividends = DividendsData(today=self.today)
        capital_gains = CapitalGainsData(today=self.today)

        stock_aggregates = AggregateStocks(
            today=self.today, previous_report_delta=previous_report_delta)
        cash_aggregates = AggregateCash(
            today=self.today, previous_report_delta=previous_report_delta)
        benchmark_aggregates = AggregateBenchmark(today=self.today)
        summary = Summary(stock_aggregates, cash_aggregates,
                          benchmark_aggregates, today=self.today)
        snapshot_aggregates = AggregateSnapshots(today=self.today)

        self.first_sheet = BuildFirstSheet(self.today, self.builder,
                                           dividends, capital_gains,
                                           stock_aggregates, cash_aggregates,
                                           benchmark_aggregates, snapshot_aggregates,
                                           summary)

        self.second_sheet = BuildSecondSheet(
            self.today, self.builder, snapshot_aggregates, benchmark_aggregates)

        self.third_sheet = BuildThirdSheet(
            self.today, self.builder, dividends)

        self.fourth_sheet = BuildFourthSheet(
            self.today, self.builder, capital_gains)

        self.fifth_sheet = BuildFifthSheet(
            self.today, self.builder, summary.nav_current
        )

        self.builder.workbook.close()


@logger.catch(reraise=True)
def main():
    """
    main function for testing
    """
    initialize_databases()
    BuildExcel()


if __name__ == '__main__':
    main()
