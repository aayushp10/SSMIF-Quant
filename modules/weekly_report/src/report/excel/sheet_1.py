#!/usr/bin/env python3
"""
Build first sheet
"""

from loguru import logger
from typing import List, Any
from datetime import date
import numpy as np
from ssmif_sdk.aggregates.cash import AggregateCash
from ssmif_sdk.aggregates.benchmark import AggregateBenchmark
from ssmif_sdk.aggregates.stocks import AggregateStocks
from ssmif_sdk.aggregates.summary import Summary
from ssmif_sdk.aggregates.transactions import AggregateTransactions
from ssmif_sdk.utils.enums import sector_type_map
from ssmif_sdk.utils.main import get_percent_change, make_uniform_shape, get_trading_date
from ssmif_sdk.utils.excel_builder import ExcelBuilder, FormatConfig, \
    NumberFormatType, HeaderType, HeaderData, BorderFormatType
from report.dividends import DividendsData
from report.capital_gains import CapitalGainsData
from report.aggregates.snapshots import AggregateSnapshots


class BuildFirstSheet:
    """
    build excel class
    """

    def __init__(self, today: date, builder: ExcelBuilder, dividends: DividendsData,
                 capital_gains: CapitalGainsData, stock_aggregates: AggregateStocks,
                 cash_aggregates: AggregateCash, benchmark_aggregates: AggregateBenchmark,
                 snapshot_aggregates: AggregateSnapshots, summary: Summary) -> None:
        logger.info('building first sheet')
        self.today = today
        self.builder = builder
        self.worksheet = self.builder.workbook.add_worksheet(
            'SMIF Position Report')

        self.builder.set_column_widths(self.worksheet, {
            1: 20, 2: 25, 3: 35, 4: 25, 5: 25, 6: 20,
            7: 20, 8: 20, 9: 20, 10: 30, 11: 15, 12: 20,
            13: 25, 14: 5, 15: 20, 16: 25
        })
        self.builder.set_row_heights(self.worksheet, {
            16: 40,
        })
        self.header_len = 15
        self.builder.shrink_first_col(self.worksheet)

        aggregate_transactions = AggregateTransactions(today=self.today)

        start_row = self.build_summary(
            summary, benchmark_aggregates, aggregate_transactions)
        start_row = self.build_snapshot(start_row, snapshot_aggregates)
        start_row = self.build_aggregate_return_stats(
            start_row, stock_aggregates, cash_aggregates, benchmark_aggregates, dividends)
        self.build_other_calculations(
            start_row, benchmark_aggregates, dividends, capital_gains, aggregate_transactions)
        logger.info('done building first sheet')

    def build_summary(self, summary: Summary, benchmark: AggregateBenchmark,
                      aggregate_transactions: AggregateTransactions) -> int:
        """
        build the summary on the first sheet
        """
        start_row = 0

        self.builder.write_section_header(
            self.worksheet, start_row, 1, self.header_len, 'portfolio summary')

        start_row += 2
        col_offset = 2

        # Current Nav

        self.worksheet.write(
            start_row, col_offset, 'current nav in $'.upper(),
            self.builder.get_format(FormatConfig(header_type=HeaderType.sub_section,
                                                 border_formats=[BorderFormatType.all])))
        self.worksheet.write(
            start_row, col_offset + 1, summary.nav_current,
            self.builder.get_format(FormatConfig(number_format_type=NumberFormatType.money,
                                                 border_formats=[BorderFormatType.all])))

        # First Table

        headers: List[HeaderData] = [
            HeaderData('', FormatConfig(bold=True)),
            HeaderData('previous report'.upper()),
            HeaderData('month open'.upper()),
            HeaderData('year open'.upper()),
        ]

        start_row += 2

        for i, header in enumerate(headers):
            col = i + col_offset
            self.worksheet.write(
                start_row, col, header.title, self.builder.get_format(
                    FormatConfig(bold=True,
                                 border_formats=[BorderFormatType.all])))

        side_headers: List[HeaderData] = [
            HeaderData('nav in $'.upper(),
                       FormatConfig(number_format_type=NumberFormatType.money,
                                    border_formats=[BorderFormatType.all])),
            HeaderData('nav change in $'.upper(),
                       FormatConfig(number_format_type=NumberFormatType.money,
                                    border_formats=[BorderFormatType.all])),
            HeaderData('nav change in %'.upper(),
                       FormatConfig(number_format_type=NumberFormatType.percent,
                                    border_formats=[BorderFormatType.all])),
        ]
        table_data: List[List[Any]] = [[] for _ in enumerate(side_headers)]
        for i, header in enumerate(side_headers):
            table_data[i].append(header.title)

        for _, nav in enumerate([summary.nav_previous, summary.nav_month, summary.nav_year]):
            table_data[0].append(nav)
            table_data[1].append(summary.nav_current - nav)
            table_data[2].append(
                get_percent_change(summary.nav_current, nav))

        start_row += 1

        for i, current_row in enumerate(table_data):
            for j, val in enumerate(current_row):
                row = start_row + i
                col = col_offset + j
                self.worksheet.write(
                    row, col, val, self.builder.get_format(side_headers[i].format if j != 0
                                                           else FormatConfig(bold=True,
                                                                             border_formats=[BorderFormatType.all])))
                if i != 0 and j != 0:
                    self.builder.add_conditional_format(
                        self.worksheet, row, col, side_headers[i].format)

        # Second Table

        start_row += 4
        self.worksheet.write(
            start_row, col_offset, 'equity & cash portfolio'.upper(),
            self.builder.get_format(FormatConfig(header_type=HeaderType.sub_section)))
        start_row += 1

        headers = [
            HeaderData('', FormatConfig(
                bold=True, border_formats=[BorderFormatType.all])),
            HeaderData('Portfolio Return',
                       FormatConfig(number_format_type=NumberFormatType.percent,
                                    border_formats=[BorderFormatType.all])),
            HeaderData('Benchmark Return *',
                       FormatConfig(number_format_type=NumberFormatType.percent,
                                    border_formats=[BorderFormatType.all])),
            HeaderData('Over / Under Perform',
                       FormatConfig(number_format_type=NumberFormatType.percent,
                                    border_formats=[BorderFormatType.all])),
        ]
        for i, header in enumerate(headers):
            col = i + col_offset
            self.worksheet.write(
                start_row, col, header.title, self.builder.get_format(
                    FormatConfig(bold=True, border_formats=[BorderFormatType.all])))

        side_headers_2: List[HeaderData] = [
            HeaderData('year to date'.upper()),
            HeaderData('month to date'.upper()),
        ]
        table_data = [[] for _ in enumerate(side_headers_2)]
        for i, header in enumerate(side_headers_2):
            table_data[i].append(header.title)

        for i, navs in enumerate([(summary.nav_year, summary.nav_month, summary.nav_current),
                                  (benchmark.year, benchmark.month, benchmark.current)]):
            table_data[0].append(get_percent_change(navs[2], navs[0]))
            table_data[1].append(get_percent_change(navs[2], navs[1]))
        for i, _ in enumerate(side_headers_2):
            table_data[i].append(table_data[i][-2] - table_data[i][-1])

        start_row += 1
        for i, current_row in enumerate(table_data):
            for j, val in enumerate(current_row):
                row = start_row + i
                col = col_offset + j
                self.worksheet.write(
                    row, col, val, self.builder.get_format(headers[j].format))
                if j != 0:
                    self.builder.add_conditional_format(
                        self.worksheet, row, col, side_headers_2[i].format)

        # Third Table: vol

        start_row += 4
        self.worksheet.write(
            start_row, col_offset, 'portfolio volatility'.upper(),
            self.builder.get_format(FormatConfig(header_type=HeaderType.sub_section)))
        start_row += 1

        headers = [
            HeaderData('', FormatConfig(bold=True,
                                        border_formats=[BorderFormatType.all])),
            HeaderData('Portfolio Annualized Volatility',
                       FormatConfig(number_format_type=NumberFormatType.percent,
                                    border_formats=[BorderFormatType.all])),
            HeaderData('Benchmark Annualized Volatility',
                       FormatConfig(number_format_type=NumberFormatType.percent,
                                    border_formats=[BorderFormatType.all])),
            HeaderData('Over / Under Perform',
                       FormatConfig(number_format_type=NumberFormatType.percent,
                                    border_formats=[BorderFormatType.all])),
            HeaderData('Portfolio Annualized Sharpe Ratio',
                       FormatConfig(number_format_type=NumberFormatType.number,
                                    border_formats=[BorderFormatType.all])),
            HeaderData('Benchmark Annualized Sharpe Ratio',
                       FormatConfig(number_format_type=NumberFormatType.number,
                                    border_formats=[BorderFormatType.all])),
        ]
        for i, header in enumerate(headers):
            col = i + col_offset
            self.worksheet.write(
                start_row, col, header.title, self.builder.get_format(
                    FormatConfig(bold=True, text_wrap=True,
                                 border_formats=[BorderFormatType.all])))
        side_headers_3: List[HeaderData] = [
            HeaderData('year to date'.upper()),
            HeaderData('month to date'.upper()),
        ]
        table_data = [[] for _ in enumerate(side_headers_3)]
        for i, header in enumerate(side_headers_3):
            table_data[i].append(header.title)

        table_data[0].extend(
            [summary.vol_portfolio_year, summary.vol_benchmark_year])
        table_data[1].extend([summary.vol_portfolio_month,
                              summary.vol_benchmark_month])
        for i, _ in enumerate(side_headers_3):
            table_data[i].append(table_data[i][2] - table_data[i][1])
        table_data[0].extend(
            [summary.sharpe_ratio_portfolio_ytd, summary.sharpe_ratio_benchmark_ytd])
        table_data[1].extend(
            [summary.sharpe_ratio_portfolio_mtd, summary.sharpe_ratio_benchmark_mtd])

        start_row += 1
        for i, current_row in enumerate(table_data):
            for j, val in enumerate(current_row):
                row = start_row + i
                col = col_offset + j
                self.worksheet.write(
                    row, col, val, self.builder.get_format(headers[j].format))
                if j == 3:
                    self.builder.add_conditional_format(
                        self.worksheet, row, col, headers[j].format)

        # Fourth Table

        start_row += 3
        self.worksheet.write(
            start_row, col_offset, 'since last month'.upper(),
            self.builder.get_format(FormatConfig(header_type=HeaderType.sub_section)))
        start_row += 1

        headers = [
            HeaderData('Positions Added', FormatConfig(
                border_formats=[BorderFormatType.all])),
            HeaderData('Positions Closed', FormatConfig(
                border_formats=[BorderFormatType.all])),
        ]
        for i, header in enumerate(headers):
            col = i + col_offset
            self.worksheet.write(
                start_row, col, header.title, self.builder.get_format(
                    FormatConfig(bold=True,
                                 border_formats=[BorderFormatType.all])))
        table_data = [aggregate_transactions.stocks_bought,
                      aggregate_transactions.stocks_sold]

        # transpose 2-d array. does not have to be uniform shape
        table_data = np.transpose(make_uniform_shape(table_data, '')).tolist()

        if len(table_data) == 0:
            num_empty_rows: int = 1
            for _ in range(num_empty_rows):
                table_data.append([''] * len(headers))

        start_row += 1
        for i, current_row in enumerate(table_data):
            for j, val in enumerate(current_row):
                row = start_row + i
                col = col_offset + j
                self.worksheet.write(
                    row, col, val, self.builder.get_format(headers[j].format))

        end_row = start_row + len(table_data)

        # Fifth Table

        start_row -= 1
        col_offset += 3
        headers = [
            HeaderData('5 YR Treasury Yield',
                       FormatConfig(number_format_type=NumberFormatType.percent,
                                    border_formats=[BorderFormatType.all])),
            HeaderData('5 YR S&P 500 CAGR',
                       FormatConfig(number_format_type=NumberFormatType.percent,
                                    border_formats=[BorderFormatType.all])),
        ]
        for i, header in enumerate(headers):
            col = i + col_offset
            self.worksheet.write(
                start_row, col, header.title, self.builder.get_format(
                    FormatConfig(bold=True,
                                 border_formats=[BorderFormatType.all])))
        table_data = [[summary.us_treasury_5_year_yields,
                       summary.benchmark_5_year_cagr]]

        start_row += 1
        for i, current_row in enumerate(table_data):
            for j, val in enumerate(current_row):
                row = start_row + i
                col = col_offset + j
                self.worksheet.write(
                    row, col, val, self.builder.get_format(headers[j].format))

        return end_row

    def build_snapshot(self, start_row: int, snapshot_aggregates: AggregateSnapshots) -> int:
        """
        build the summary on the first sheet
        """
        row = start_row + 2

        self.builder.write_section_header(
            self.worksheet, row, 1, self.header_len,
            'detailed portfolio snapshot')

        row += 1
        col_offset = 2

        snapshots = snapshot_aggregates.snapshots

        self.worksheet.write(
            row, col_offset + 8, get_trading_date(self.today),
            self.builder.get_format(FormatConfig(number_format_type=NumberFormatType.date)))
        self.worksheet.write(
            row, col_offset + 10, snapshots[0].month_open,
            self.builder.get_format(FormatConfig(number_format_type=NumberFormatType.date)))
        self.worksheet.write(
            row, col_offset + 13, snapshots[0].year_open,
            self.builder.get_format(FormatConfig(number_format_type=NumberFormatType.date)))

        row += 1

        # order matters for writing
        headers: List[HeaderData] = [
            HeaderData('Ticker'),
            HeaderData('Company'),
            HeaderData('Sector'),
            HeaderData(
                'Original Purchase Date',
                FormatConfig(number_format_type=NumberFormatType.date)),
            HeaderData('Shares'),
            HeaderData('Entry VWAP',
                       FormatConfig(number_format_type=NumberFormatType.money)),
            HeaderData('Most Recent Price',
                       FormatConfig(number_format_type=NumberFormatType.money)),
            HeaderData('Invested Amount',
                       FormatConfig(number_format_type=NumberFormatType.money)),
            HeaderData(
                'Current Value (Mark-to-Market)',
                FormatConfig(number_format_type=NumberFormatType.money)),
            HeaderData(''),
            HeaderData('Month Open Price',
                       FormatConfig(number_format_type=NumberFormatType.money)),
            HeaderData(
                'Month Open Position Value',
                FormatConfig(number_format_type=NumberFormatType.money)),
            HeaderData(''),
            HeaderData('Year Open Price',
                       FormatConfig(number_format_type=NumberFormatType.money)),
            HeaderData(
                'Year Open Position Value',
                FormatConfig(number_format_type=NumberFormatType.money))
        ]
        for i, header in enumerate(headers):
            col = i + col_offset
            self.worksheet.write(
                row, col, header.title, self.builder.get_format(FormatConfig(bold=True)))

        row += 1

        for i, snapshot in enumerate(snapshots):
            ordered_data: List[Any] = [snapshot.ticker, snapshot.company, sector_type_map[snapshot.sector],
                                       snapshot.date, snapshot.shares, snapshot.vwap,
                                       snapshot.most_recent_price, snapshot.invested_amount, snapshot.current_value_mtm,
                                       snapshot.month_open_price, snapshot.month_open_value, snapshot.year_open_price,
                                       snapshot.year_open_value]
            current_header: int = 0
            for data in ordered_data:
                while current_header < len(headers) and len(headers[current_header].title) == 0:
                    current_header += 1
                if current_header == len(headers):
                    break
                self.worksheet.write(
                    row + i, current_header + col_offset, data, self.builder.get_format(headers[current_header].format))
                current_header += 1

        row += len(snapshots)

        self.worksheet.write(
            row, col_offset + 6, 'Total', self.builder.get_format(FormatConfig(bold=True)))
        totals_format = FormatConfig(bold=True, number_format_type=NumberFormatType.money,
                                     border_formats=[BorderFormatType.top, BorderFormatType.bottom])
        self.worksheet.write(row, col_offset + 7, snapshot_aggregates.total_invested_amount,
                             self.builder.get_format(totals_format))
        self.worksheet.write(row, col_offset + 8, snapshot_aggregates.total_value_mtm,
                             self.builder.get_format(totals_format))
        self.worksheet.write(row, col_offset + 11, snapshot_aggregates.total_month_open,
                             self.builder.get_format(totals_format))
        self.worksheet.write(row, col_offset + 14, snapshot_aggregates.total_year_open,
                             self.builder.get_format(totals_format))

        end_row = row + 2
        return end_row

    def build_aggregate_return_stats(self, start_row: int, stock_aggregates: AggregateStocks,
                                     cash_aggregates: AggregateCash, benchmark: AggregateBenchmark,
                                     dividends: DividendsData) -> int:
        """
        create aggregate return statistics section
        """
        start_row += 2
        self.builder.write_section_header(
            self.worksheet, start_row, 1, self.header_len, 'aggregate portfolio return statistics')

        col_offset = 2

        start_row += 2
        headers: List[HeaderData] = [
            HeaderData('year open'.upper()),
            HeaderData('month open'.upper()),
            HeaderData('most recent close'.upper()),
        ]
        side_headers: List[HeaderData] = [
            HeaderData('Cash Balance'),
            HeaderData('Securities Value'),
            HeaderData('Dividends'),
            HeaderData('New Asset Value'),
        ]

        formats: List[FormatConfig] = [
            FormatConfig(),
            FormatConfig(number_format_type=NumberFormatType.date),
            FormatConfig(number_format_type=NumberFormatType.money)
        ]

        dates: List[date] = [benchmark.year_open, benchmark.month_open,
                             benchmark.most_recent_trading_day]
        cash_balances: List[float] = [cash_aggregates.year,
                                      cash_aggregates.month, cash_aggregates.current]
        securities_values: List[float] = [stock_aggregates.year,
                                          stock_aggregates.month, stock_aggregates.current]
        dividends_values: List[float] = [
            0, dividends.month_open, dividends.year_total]

        for i, header in enumerate(headers):
            self.worksheet.write(
                start_row, col_offset, header.title,
                self.builder.get_format(FormatConfig(bold=True)))
            table_data: List[List[Any]] = [[] for _ in enumerate(side_headers)]
            for j, side_header in enumerate(side_headers):
                table_data[j].append(side_header.title)
                table_data[j].append(dates[i])
            table_data[0].append(cash_balances[i])
            table_data[1].append(securities_values[i])
            table_data[2].append(dividends_values[i])
            table_data[3].append(cash_balances[i] + securities_values[i])

            col_offset += 1

            for j, current_row in enumerate(table_data):
                for k, val in enumerate(current_row):
                    row = start_row + j
                    col = col_offset + k
                    current_format = formats[k]
                    if j == len(table_data) - 1:
                        current_format.border_formats = [BorderFormatType.top]
                    else:
                        current_format.border_formats = []
                    self.worksheet.write(
                        row, col, val, self.builder.get_format(current_format))

            col_offset -= 1
            start_row += len(table_data) + 2

        end_row = start_row + 1

        return end_row

    def build_other_calculations(self, start_row: int, benchmark: AggregateBenchmark,
                                 dividends: DividendsData, capital_gains: CapitalGainsData,
                                 aggregate_transactions: AggregateTransactions) -> None:
        """
        create other calculations section
        """
        start_row += 1
        self.builder.write_section_header(
            self.worksheet, start_row, 1, self.header_len, 'other calculations')

        col_offset = 1
        start_row += 2

        # Table 1

        self.worksheet.write(
            start_row, col_offset, 'benchmark'.upper(),
            self.builder.get_format(FormatConfig(bold=True)))
        start_row += 1

        side_headers: List[HeaderData] = [
            HeaderData('S&P 500 Year Open'),
            HeaderData('S&P 500 Month Open'),
            HeaderData('S&P 500 Most Recent Close'),
        ]
        formats: List[FormatConfig] = [
            FormatConfig(),
            FormatConfig(number_format_type=NumberFormatType.date),
            FormatConfig(number_format_type=NumberFormatType.money)
        ]

        dates: List[date] = [benchmark.year_open, benchmark.month_open,
                             benchmark.most_recent_trading_day]
        benchmark_values: List[float] = [
            benchmark.year, benchmark.month, benchmark.current]

        table_data: List[List[Any]] = [[] for _ in enumerate(side_headers)]
        for i, side_header in enumerate(side_headers):
            table_data[i].append(side_header.title)
            table_data[i].append(dates[i])
            table_data[i].append(benchmark_values[i])

        col_offset += 1

        for i, current_row in enumerate(table_data):
            for j, val in enumerate(current_row):
                row = start_row + i
                col = col_offset + j
                self.worksheet.write(
                    row, col, val, self.builder.get_format(formats[j]))

        col_offset -= 1
        start_row += len(table_data) + 1

        # Table 2

        side_headers = [
            HeaderData('MTD Benchmark Return'),
            HeaderData('YTD Benchmark Return'),
        ]
        formats = [
            FormatConfig(bold=True),
            FormatConfig(),
            FormatConfig(number_format_type=NumberFormatType.percent)
        ]
        benchmark_returns: List[float] = [
            benchmark.month_return,
            benchmark.year_return
        ]

        table_data = [[] for _ in enumerate(side_headers)]
        for i, side_header in enumerate(side_headers):
            table_data[i].append(side_header.title)
            table_data[i].append('')
            table_data[i].append(benchmark_returns[i])

        col_offset += 1

        for i, current_row in enumerate(table_data):
            for j, val in enumerate(current_row):
                row = start_row + i
                col = col_offset + j
                self.worksheet.write(
                    row, col, val, self.builder.get_format(formats[j]))

        col_offset -= 1
        start_row += len(table_data) + 1

        # Table 3

        self.worksheet.write(
            start_row, col_offset, 'dividends'.upper(),
            self.builder.get_format(FormatConfig(bold=True)))
        start_row += 1

        side_headers = [
            HeaderData('Monthly Accrued Dividends'),
            HeaderData('Annual Accrued Dividends'),
        ]
        formats = [
            FormatConfig(),
            FormatConfig(),
            FormatConfig(number_format_type=NumberFormatType.money)
        ]
        dividend_values: List[float] = [
            dividends.sums[self.today.month - 1], dividends.year_total]

        table_data = [[] for _ in enumerate(side_headers)]
        for i, side_header in enumerate(side_headers):
            table_data[i].append(side_header.title)
            table_data[i].append('')
            table_data[i].append(dividend_values[i])

        col_offset += 1

        for i, current_row in enumerate(table_data):
            for j, val in enumerate(current_row):
                row = start_row + i
                col = col_offset + j
                self.worksheet.write(
                    row, col, val, self.builder.get_format(formats[j]))

        col_offset -= 1
        start_row += len(table_data) + 1

        # Table 4

        self.worksheet.write(
            start_row, col_offset, 'capital gains'.upper(),
            self.builder.get_format(FormatConfig(bold=True)))
        start_row += 1

        side_headers = [
            HeaderData('Monthly Capital Gains'),
            HeaderData('Annual Capital Gains'),
        ]
        formats = [
            FormatConfig(),
            FormatConfig(),
            FormatConfig(number_format_type=NumberFormatType.money)
        ]
        capital_gains_data: List[float] = [
            capital_gains.sums[self.today.month - 1],
            capital_gains.year_total
        ]

        table_data = [[] for _ in enumerate(side_headers)]
        for i, side_header in enumerate(side_headers):
            table_data[i].append(side_header.title)
            table_data[i].append('')
            table_data[i].append(capital_gains_data[i])

        col_offset += 1

        for i, current_row in enumerate(table_data):
            for j, val in enumerate(current_row):
                row = start_row + i
                col = col_offset + j
                self.worksheet.write(
                    row, col, val, self.builder.get_format(formats[j]))

        col_offset -= 1
        start_row += len(table_data) + 1

        # Table 5

        self.worksheet.write(
            start_row, col_offset, 'deposits'.upper(),
            self.builder.get_format(FormatConfig(bold=True)))
        start_row += 1

        side_headers = [
            HeaderData('Monthly Deposits'),
            HeaderData('Monthly Withdrawals'),
            HeaderData('Annual Net Deposits'),
        ]
        formats = [
            FormatConfig(),
            FormatConfig(),
            FormatConfig(number_format_type=NumberFormatType.money)
        ]

        deposit_withdrawal_data: List[float] = [
            aggregate_transactions.monthly_deposits,
            aggregate_transactions.monthly_withdrawals,
            aggregate_transactions.annual_deposits -
            aggregate_transactions.annual_withdrawals
        ]

        table_data = [[] for _ in enumerate(side_headers)]
        for i, side_header in enumerate(side_headers):
            table_data[i].append(side_header.title)
            table_data[i].append('')
            table_data[i].append(deposit_withdrawal_data[i])

        col_offset += 1

        for i, current_row in enumerate(table_data):
            for j, val in enumerate(current_row):
                row = start_row + i
                col = col_offset + j
                self.worksheet.write(
                    row, col, val, self.builder.get_format(formats[j]))

        col_offset -= 1
        start_row += len(table_data) + 1

        # line at the end

        self.builder.write_section_header(
            self.worksheet, start_row, 1, self.header_len, '')
