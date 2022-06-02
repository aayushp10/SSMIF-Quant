#!/usr/bin/env python3
"""
    Operations object
"""
from __future__ import annotations
#################################
# for handling relative imports #
#################################
if __name__ == '__main__':
    import sys
    from pathlib import Path
    current_file = Path(__file__).resolve()
    root = next(elem for elem in current_file.parents
                if str(elem).endswith('src'))
    sys.path.append(str(root))
    # remove the current file's directory from sys.path
    try:
        sys.path.remove(str(current_file.parent))
    except ValueError:  # Already removed
        pass

from typing import List, Dict, Any

from classes.normalized_column import NormalizedColumn

from operations.operations_functions import FunctionType

from utils.enums import DataSource, SectorType


class Operation:
    data_source_type = DataSource.operations

    def __init__(self, sector_type: SectorType,
                 output_columns: List[str],
                 operation_type: str,
                 input_columns: List[Dict[str, str]],
                 arguments: Dict[str, Any],
                 remove: List[str]):
        if not FunctionType.has_value(operation_type):
            raise ValueError(f'invalid operation {operation_type} provided')
        self.type = FunctionType(operation_type)
        self.arguments: Dict[str, Any] = arguments
        self.remove: List[str] = remove
        self.input_columns: List[NormalizedColumn] = []
        self.output_columns: List[NormalizedColumn] = []

        for input_col in input_columns:
            self.input_columns.append(
                NormalizedColumn.from_dict(sector_type, input_col))

        for output_col in output_columns:
            self.output_columns.append(NormalizedColumn(
                DataSource.operations, sector_type.name, output_col))

    @classmethod
    def from_dict(cls, input_dict: Dict[str, str]) -> Operation:
        """
        constructor for operation from dict
        """
        output_columns_key = 'output_columns'
        operation_type_key = 'operation'
        input_columns_key = 'input_columns'
        arguments_key = 'arguments'
        remove_columns_key = 'remove'

        return cls(input_dict[output_columns_key],
                   input_dict[operation_type_key],
                   input_dict[input_columns_key],
                   input_dict.get(arguments_key, {}),
                   input_dict.get(remove_columns_key, []))
