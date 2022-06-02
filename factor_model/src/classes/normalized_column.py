#!/usr/bin/env python3
"""
Normalized Column Object
"""

from __future__ import annotations

from typing import Dict
from utils.enums import DataSource, SectorType
from utils.utils import data_source_prepend_map, normalize_str


class NormalizedColumn:
    colname_split_char: str = ':'

    def __init__(self, data_source: DataSource, name: str, column_name: str):
        """
        data_source = bb for bloomberg
        name = the tickername 
        column_name = the actual name of the column (original)
        """
        self.data_source = data_source
        self.name = name
        self.column_name = column_name

    @classmethod
    def from_str(cls, input_str: str) -> NormalizedColumn:
        """
        constructor from the full name of the column
        """
        split_data = input_str.split(cls.colname_split_char)
        data_source = DataSource(
            data_source_prepend_map.inverse[split_data[0]])
        name = split_data[1]
        column_name = split_data[2]
        return cls(data_source, name, column_name)

    @classmethod
    def from_dict(cls, sector_type: SectorType, raw_column: Dict[str, str]) -> NormalizedColumn:
        """
        constructor from the full name of the column
        returns: (something like) B_XLK_US_EQUITY_PUT_CALL_OPEN_INTEREST
        """
        # keys
        data_source_key = 'source'
        name_key = 'ticker'
        column_name_key = 'col_name'
        data_source_raw: str = raw_column[data_source_key]
        if not DataSource.has_value(data_source_raw):
            raise ValueError(f'invalid data source {data_source_raw} provided')
        data_source = DataSource(data_source_raw)

        if data_source == DataSource.operations:
            raw_column[name_key] = sector_type.name

        return cls(data_source, raw_column[name_key], raw_column[column_name_key])

    def normalize_colname(self) -> str:
        """
        name = tickername / normal name
        bb{colname_split_char}xlk_us_equity{colname_split_char}px_last
        XLK US EQUITY   -> xlk_us_equity
        """
        path_prepend = data_source_prepend_map[self.data_source]
        return self.colname_split_char.join([path_prepend, normalize_str(self.name), normalize_str(self.column_name)])
