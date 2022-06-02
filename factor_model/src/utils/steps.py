#!/usr/bin/env python3
"""
step type
"""

from enum import Enum
from typing import Any, Set, List


class StepType(Enum):
    """
    Enum to store step types
    """
    load = "load"
    clean = "clean"
    viz = "viz"

    @classmethod
    def has_value(cls, value: Any) -> bool:
        """
        Return true / false for whether the input is stored as a value in the enum
        """
        values = StepType.get_values()
        return value in values

    @classmethod
    def get_values(cls) -> Set[Any]:
        """
        Return a list of the values stored within the enum
        """
        return set(item.value for item in cls)


skip_order: List[StepType] = [
    StepType.load, StepType.clean, StepType.viz
]
