#!/usr/bin/env python3
"""
Window file
"""
# Import necessary packages
from __future__ import annotations

from datetime import datetime
from typing import Dict, Any

from constants import date_format


class Window:
    """
    Window object for time frames of data
    """
    # Initialize parameters for Window class

    def __init__(self, start_date: datetime, end_date: datetime):
        self.start_date = start_date
        self.end_date = end_date

    @classmethod
    def from_dict(cls, input_dict: Dict[str, Any]) -> Window:
        """
        constructor from the full name of the column
        """
        # keys
        start_date_key = 'start_date'
        end_date_key = 'end_date'

        start_date = datetime.strptime(
            str(input_dict[start_date_key]), date_format)
        end_date = datetime.strptime(
            str(input_dict[end_date_key]), date_format)

        return cls(start_date, end_date)
