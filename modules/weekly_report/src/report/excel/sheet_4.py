#!/usr/bin/env python3
"""
Build fourth sheet
"""

from loguru import logger
from typing import List, Any
from calendar import month_name
from datetime import date
from ssmif_sdk.utils.excel_builder import ExcelBuilder, FormatConfig, \
    NumberFormatType, HeaderData, BorderFormatType, HorizontalAlignmentFormatType
from report.capital_gains import CapitalGainsData


class BuildFourthSheet:
    """
    build excel class
    """

    def __init__(self, today: date, builder: ExcelBuilder, capital_gains: CapitalGainsData):
        logger.info('building fourth sheet')
        self.today = today
        self.builder = builder
        self.worksheet = self.builder.workbook.add_worksheet('Capital Gains')

        self.builder.set_column_widths(self.worksheet, {
            1: 20, 2: 35, 3: 15, 4: 15, 5: 15, 6: 15, 7: 15,
            8: 15, 9: 15, 10: 15
        })
        self.builder.shrink_first_col(self.worksheet)
        self.build_capital_gains(capital_gains)
        logger.info('done building fourth sheet')

    def build_capital_gains(self, capital_gains: CapitalGainsData) -> None:
        """
        create capital gains section
        """
        row = 1
        col_offset = 1

        months = [month_name[i + 1] for i in range(self.today.month)]
        headers: List[HeaderData] = [
            HeaderData('Ticker'),
            HeaderData('Company'),
            HeaderData('Original Purchase Date',
                       FormatConfig(number_format_type=NumberFormatType.date)),
            HeaderData('Date of Sale',
                       FormatConfig(number_format_type=NumberFormatType.date)),
            HeaderData('Shares'),
            HeaderData('Entry Price',
                       FormatConfig(number_format_type=NumberFormatType.money)),
            HeaderData('Invested Amount',
                       FormatConfig(number_format_type=NumberFormatType.money)),
            HeaderData('Price at Sale',
                       FormatConfig(number_format_type=NumberFormatType.money)),
            HeaderData('Value at Sale',
                       FormatConfig(number_format_type=NumberFormatType.money)),
            HeaderData('Total Capital Gain', has_conditional=True,
                       formatter=FormatConfig(number_format_type=NumberFormatType.money)),
        ]

        capital_gains_data = capital_gains.capital_gains

        min_num_capital_gains: int = 2

        for i, month in enumerate(months):
            self.builder.write_section_header(
                self.worksheet, row, 1, len(headers) - 2, month)
            row += 2

            self.builder.set_row_heights(self.worksheet, {
                row - 1: 5,
                row: 30
            })
            for j, header in enumerate(headers):
                col = j + col_offset
                self.worksheet.write(
                    row, col, header.title, self.builder.get_format(
                        FormatConfig(bold=True, text_wrap=True,
                                     border_formats=[BorderFormatType.bottom])))
            row += 1

            table_data: List[List[Any]] = []
            for capital_gains_elem in capital_gains_data[i]:
                table_data.append([capital_gains_elem.ticker, capital_gains_elem.company,
                                   capital_gains_elem.purchase_date, capital_gains_elem.sell_date,
                                   capital_gains_elem.shares, capital_gains_elem.entry_price,
                                   capital_gains_elem.invested_value, capital_gains_elem.sell_price,
                                   capital_gains_elem.sell_value, capital_gains_elem.capital_gains])

            for row_data in table_data:
                for j, val in enumerate(row_data):
                    col = j + col_offset
                    self.worksheet.write(
                        row, col, val, self.builder.get_format(headers[j].format))
                    if headers[j].has_conditional:
                        self.builder.add_conditional_format(
                            self.worksheet, row, col, headers[i].format)
                row += 1

            num_empty_rows = max(0, min_num_capital_gains - len(table_data))
            row += num_empty_rows

            # write totals row
            totals_row: List[Any] = [''] * 6
            totals_row.append(
                f'Total Capital Gains for {month} {self.today.year}')
            totals_row.extend([''] * 2)
            totals_row.append(capital_gains.sums[i])

            for j, val in enumerate(totals_row):
                col = j + col_offset
                format_obj = FormatConfig(
                    border_formats=[BorderFormatType.top], border_style=6)
                if j == len(totals_row) - 1:
                    format_obj.number_format_type = NumberFormatType.money
                else:
                    format_obj.horizontal_alignment = HorizontalAlignmentFormatType.left
                self.worksheet.write(
                    row, col, val, self.builder.get_format(format_obj))
                if j == len(totals_row) - 1:
                    self.builder.add_conditional_format(
                        self.worksheet, row, col, format_obj)

            row += 2
