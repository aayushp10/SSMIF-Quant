#!/usr/bin/env python3
"""
Build third sheet
"""

from loguru import logger
from typing import List, Any
from calendar import month_name
from datetime import date
from ssmif_sdk.utils.excel_builder import ExcelBuilder, FormatConfig, \
    NumberFormatType, HeaderData, BorderFormatType
from report.dividends import DividendsData


class BuildThirdSheet:
    """
    build excel class
    """

    def __init__(self, today: date, builder: ExcelBuilder, dividends: DividendsData):
        logger.info('building third sheet')
        self.today = today
        self.builder = builder
        self.worksheet = self.builder.workbook.add_worksheet('Dividends')

        self.builder.set_column_widths(self.worksheet, {
            1: 35, 2: 25, 3: 25, 4: 25,
        })
        self.builder.shrink_first_col(self.worksheet)
        self.build_dividends(dividends)
        logger.info('done building third sheet')

    def build_dividends(self, dividends: DividendsData) -> None:
        """
        create aggregate return statistics section
        """
        row = 1
        col_offset = 1

        months = [month_name[i + 1] for i in range(self.today.month)]
        headers: List[HeaderData] = [
            HeaderData('Ticker', FormatConfig(
                border_formats=[BorderFormatType.all])),
            HeaderData('Company', FormatConfig(
                border_formats=[BorderFormatType.all])),
            HeaderData('Dividend Date',
                       FormatConfig(number_format_type=NumberFormatType.date,
                                    border_formats=[BorderFormatType.all])),
            HeaderData('Dividend Amount',
                       FormatConfig(number_format_type=NumberFormatType.money,
                                    border_formats=[BorderFormatType.all]))
        ]

        dividends_data = dividends.dividends

        min_num_dividends: int = 5

        for i, month in enumerate(months):
            self.builder.write_section_header(
                self.worksheet, row, 1, 2, month)
            row += 1
            for j, header in enumerate(headers):
                col = j + col_offset
                self.worksheet.write(
                    row, col, header.title, self.builder.get_format(
                        FormatConfig(bold=True,
                                     border_formats=[BorderFormatType.all])))
            row += 1

            table_data: List[List[Any]] = []
            for dividend_data in dividends_data[i]:
                table_data.append([dividend_data.ticker, dividend_data.company,
                                   dividend_data.allocation_date, dividend_data.amount])
            num_empty_rows = max(0, min_num_dividends - len(table_data))
            for _ in range(num_empty_rows):
                table_data.append([''] * len(headers))
            table_data.append(
                [f'Total for {month} {self.today.year}', '', '', dividends.sums[i]])

            for row_data in table_data:
                for j, val in enumerate(row_data):
                    col = j + col_offset
                    self.worksheet.write(
                        row, col, val, self.builder.get_format(headers[j].format))
                row += 1

            row += 2
