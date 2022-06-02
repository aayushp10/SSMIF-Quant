#!/usr/bin/env python3
"""
Build fifth sheet
"""

from loguru import logger
from datetime import date
from typing import List, Any
from report.asset_allocation import AssetAllocation
from ssmif_sdk.utils.enums import sector_type_map
from ssmif_sdk.utils.excel_builder import ExcelBuilder, FormatConfig, HeaderData, \
    NumberFormatType, BorderFormatType, ConditionalFormatType


class BuildFifthSheet:
    """
    build excel class
    """

    def __init__(self, today: date, builder: ExcelBuilder, total_portfolio_value: float):
        logger.info('building fifth sheet')
        self.today = today
        self.builder = builder
        self.worksheet = self.builder.workbook.add_worksheet(
            'Asset Allocation')

        self.builder.set_column_widths(self.worksheet, {
            0: 10, 1: 20, 2: 15, 3: 20, 4: 15, 5: 15,
            6: 15, 7: 15, 8: 15, 9: 15
        })
        self.builder.set_row_heights(self.worksheet, {
            0: 5,
            1: 30
        })
        self.header_len = 14
        self.build_asset_allocation(total_portfolio_value)
        logger.info('done building fifth sheet')

    def build_asset_allocation(self, total_portfolio_value: float) -> None:
        """
        create detailed returns section
        """
        row = 1
        col_offset = 1
        date_formatted = self.today.strftime('%B %d, %Y')
        self.builder.write_section_header(
            self.worksheet, row, col_offset, self.header_len,
            f'As of {date_formatted}', uppercase=False)
        row += 2

        asset_allocations = AssetAllocation(total_portfolio_value)

        headers: List[HeaderData] = [
            HeaderData('Sector', FormatConfig(
                border_formats=[BorderFormatType.all])),
            HeaderData('Ticker', FormatConfig(
                border_formats=[BorderFormatType.all])),
            HeaderData('Portfolio Weights',
                       FormatConfig(border_formats=[BorderFormatType.all],
                                    number_format_type=NumberFormatType.percent)),
            HeaderData('Factor Model Weights',
                       FormatConfig(border_formats=[BorderFormatType.all],
                                    number_format_type=NumberFormatType.percent)),
            HeaderData('Relative Weight', has_conditional=True,
                       formatter=FormatConfig(border_formats=[BorderFormatType.all])),
            HeaderData('Difference',
                       FormatConfig(border_formats=[BorderFormatType.all],
                                    number_format_type=NumberFormatType.percent)),
            HeaderData('VOO',
                       FormatConfig(border_formats=[BorderFormatType.all],
                                    number_format_type=NumberFormatType.money)),
            HeaderData('Holdings',
                       FormatConfig(border_formats=[BorderFormatType.all],
                                    number_format_type=NumberFormatType.money)),
            HeaderData('Total',
                       FormatConfig(border_formats=[BorderFormatType.all],
                                    number_format_type=NumberFormatType.money)),
        ]

        for i, header in enumerate(headers):
            col = i + col_offset
            self.worksheet.write(
                row, col, header.title, self.builder.get_format(FormatConfig(
                    bold=True, border_formats=[BorderFormatType.all])))
        row += 1

        # sort by portfolio weights
        asset_allocations.allocations.sort(reverse=True,
                                           key=lambda allocation: allocation.portfolio_weight)

        for i, allocation in enumerate(asset_allocations.allocations):
            ordered_data: List[Any] = [sector_type_map[allocation.sector], allocation.sector_ticker, allocation.portfolio_weight,
                                       allocation.factor_model_weight,
                                       allocation.portfolio_factor_model_underweight, allocation.portfolio_factor_model_difference,
                                       allocation.benchmark_value, allocation.holdings_value, allocation.total]
            for j, data in enumerate(ordered_data):
                if headers[j].has_conditional:
                    headers[j].format.conditional_format_type = ConditionalFormatType.positive \
                        if data == 1 else ConditionalFormatType.negative
                    data = 'Underweight' if data == 1 else 'Overweight'
                self.worksheet.write(
                    row + i, j + col_offset, data, self.builder.get_format(headers[j].format))

        row += len(asset_allocations.allocations)

        self.worksheet.write(
            row, col_offset + 1, asset_allocations.total_portfolio_weights, self.builder.get_format(
                FormatConfig(bold=True, number_format_type=NumberFormatType.percent)))

        row += 4
        self.builder.set_row_heights(self.worksheet, {
            row - 1: 5,
            row: 30
        })

        self.builder.write_section_header(
            self.worksheet, row, col_offset, self.header_len,
            'Benchmark Relative Weighting', uppercase=False)

        row += 2

        headers = [
            HeaderData('Sector',
                       FormatConfig(border_formats=[BorderFormatType.all])),
            HeaderData('S&P 500 Weights',
                       FormatConfig(number_format_type=NumberFormatType.percent,
                                    border_formats=[BorderFormatType.all])),
            HeaderData('Relative Weight', has_conditional=True,
                       formatter=FormatConfig(border_formats=[BorderFormatType.all])),
            HeaderData('Difference',
                       FormatConfig(number_format_type=NumberFormatType.percent,
                                    border_formats=[BorderFormatType.all])),
        ]

        for i, header in enumerate(headers):
            col = i + col_offset
            self.worksheet.write(
                row, col, header.title, self.builder.get_format(FormatConfig(
                    bold=True, border_formats=[BorderFormatType.all])))
        row += 1

        # uncomment to sort by benchmark weights
        # asset_allocations.allocations.sort(reverse=True,
        #                                   key=lambda allocation: allocation.benchmark_weight)

        for i, allocation in enumerate(asset_allocations.allocations):
            ordered_data_allocation: List[Any] = [sector_type_map[allocation.sector], allocation.benchmark_weight,
                                                  allocation.portfolio_benchmark_underweight, allocation.portfolio_benchmark_difference]
            for j, data in enumerate(ordered_data_allocation):
                if headers[j].has_conditional:
                    headers[j].format.conditional_format_type = ConditionalFormatType.positive \
                        if data == 1 else ConditionalFormatType.negative
                    data = 'Underweight' if data == 1 else 'Overweight'
                self.worksheet.write(
                    row + i, j + col_offset, data, self.builder.get_format(headers[j].format))

        row += len(asset_allocations.allocations)

        self.worksheet.write(
            row, col_offset + 1, asset_allocations.total_benchmark_weights, self.builder.get_format(
                FormatConfig(bold=True, number_format_type=NumberFormatType.percent)))
