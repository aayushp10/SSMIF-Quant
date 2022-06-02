#!/usr/bin/env python3
"""
Build second sheet
"""

from loguru import logger
from datetime import date
from typing import List, Any
from ssmif_sdk.aggregates.benchmark import AggregateBenchmark
from ssmif_sdk.utils.excel_builder import ExcelBuilder, FormatConfig, HeaderData, \
    NumberFormatType, BorderFormatType
from ssmif_sdk.utils.enums import sector_type_map
from report.aggregates.detailed_portfolio_returns import DeltailedPortfolioReturns
from report.aggregates.snapshots import AggregateSnapshots


class BuildSecondSheet:
    """
    build excel class
    """

    def __init__(self, today: date, builder: ExcelBuilder, snapshot_aggregates: AggregateSnapshots,
                 benchmark_aggregates: AggregateBenchmark) -> None:
        logger.info('building second sheet')
        self.today = today
        self.builder = builder
        self.worksheet = self.builder.workbook.add_worksheet(
            'Detailed Returns')

        self.builder.set_column_widths(self.worksheet, {
            1: 15, 2: 35, 3: 25, 4: 15, 5: 15, 6: 15, 7: 3,
            8: 15, 9: 15, 10: 3, 11: 15, 12: 15, 13: 15
        })
        self.builder.set_row_heights(self.worksheet, {
            2: 30
        })
        self.builder.shrink_first_col(self.worksheet)
        self.header_len = 14
        self.build_detailed_returns(snapshot_aggregates, benchmark_aggregates)
        logger.info('done building second sheet')

    def build_detailed_returns(self, snapshot_aggregates: AggregateSnapshots,
                               benchmark_aggregates: AggregateBenchmark) -> None:
        """
        create detailed returns section
        """
        row = 0
        col_offset = 1
        self.builder.write_section_header(
            self.worksheet, row, col_offset, self.header_len, 'detailed portfolio returns')
        row += 1

        detailed_portfolio_returns = DeltailedPortfolioReturns(
            snapshot_aggregates, benchmark_aggregates)
        portfolio_returns = detailed_portfolio_returns.portfolio_returns

        self.worksheet.write(
            row, col_offset + 4, 'month to date'.upper(),
            self.builder.get_format(FormatConfig(bold=True)))
        self.worksheet.write(
            row, col_offset + 7, 'year to date'.upper(),
            self.builder.get_format(FormatConfig(bold=True)))
        self.worksheet.write(
            row, col_offset + 10, 'life to date'.upper(),
            self.builder.get_format(FormatConfig(bold=True)))

        row += 1

        headers: List[HeaderData] = [
            HeaderData('Ticker'),
            HeaderData('Company'),
            HeaderData('Sector'),
            HeaderData(
                'Original Purchase Date',
                FormatConfig(number_format_type=NumberFormatType.date)),
            HeaderData('Equity Return', has_conditional=True,
                       formatter=FormatConfig(number_format_type=NumberFormatType.percent)),
            HeaderData('Over / Under Perform', has_conditional=True,
                       formatter=FormatConfig(number_format_type=NumberFormatType.percent)),
            HeaderData(''),
            HeaderData('Equity Return', has_conditional=True,
                       formatter=FormatConfig(number_format_type=NumberFormatType.percent)),
            HeaderData('Over / Under Perform', has_conditional=True,
                       formatter=FormatConfig(number_format_type=NumberFormatType.percent)),
            HeaderData(''),
            HeaderData('Equity Return', has_conditional=True,
                       formatter=FormatConfig(number_format_type=NumberFormatType.percent)),
            HeaderData('Over / Under Perform', has_conditional=True,
                       formatter=FormatConfig(number_format_type=NumberFormatType.percent)),
            HeaderData('S&P 500 Index Return',
                       FormatConfig(number_format_type=NumberFormatType.percent))
        ]

        for i, header in enumerate(headers):
            col = i + col_offset
            self.worksheet.write(
                row, col, header.title, self.builder.get_format(FormatConfig(
                    bold=True, text_wrap=True)))

        row += 1

        for i, current_returns in enumerate(portfolio_returns):
            ordered_data: List[Any] = [current_returns.ticker, current_returns.company,
                                       sector_type_map[current_returns.sector], current_returns.date,
                                       current_returns.month_equity_return, current_returns.month_compare,
                                       current_returns.year_equity_return, current_returns.year_compare,
                                       current_returns.life_equity_return, current_returns.life_compare,
                                       current_returns.benchmark_life_return]
            current_header: int = 0
            for data in ordered_data:
                while current_header < len(headers) and len(headers[current_header].title) == 0:
                    current_header += 1
                if current_header == len(headers):
                    break
                self.worksheet.write(
                    row + i, current_header + col_offset, data, self.builder.get_format(headers[current_header].format))
                if headers[current_header].has_conditional:
                    self.builder.add_conditional_format(
                        self.worksheet, row + i, current_header + col_offset, headers[current_header].format)
                current_header += 1

        row += len(portfolio_returns)

        row += 1
        self.builder.set_row_heights(self.worksheet, {
            row: 5,
        })
        row += 1

        col = col_offset + 3
        self.worksheet.write(
            row, col, 'Total Portfolio', self.builder.get_format(FormatConfig(bold=True)))
        totals_format = FormatConfig(bold=True, number_format_type=NumberFormatType.percent,
                                     border_formats=[
                                         BorderFormatType.top, BorderFormatType.bottom],
                                     border_style=6)

        col += 1
        self.worksheet.write(
            row, col, detailed_portfolio_returns.month_equity_return)
        self.builder.add_conditional_format(
            self.worksheet, row, col, totals_format)
        col += 1
        self.worksheet.write(
            row, col, detailed_portfolio_returns.month_compare)
        self.builder.add_conditional_format(
            self.worksheet, row, col, totals_format)

        col += 2
        self.worksheet.write(
            row, col, detailed_portfolio_returns.year_equity_return)
        self.builder.add_conditional_format(
            self.worksheet, row, col, totals_format)
        col += 1
        self.worksheet.write(row, col, detailed_portfolio_returns.year_compare)
        self.builder.add_conditional_format(
            self.worksheet, row, col, totals_format)

        col += 2
        self.worksheet.write(
            row, col, detailed_portfolio_returns.equity_life_return)
        self.builder.add_conditional_format(
            self.worksheet, row, col, totals_format)
