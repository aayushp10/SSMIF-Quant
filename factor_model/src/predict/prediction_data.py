#!/usr/bin/env python3
"""
prediction black litterman config
"""

from __future__ import annotations
from typing import Dict
from utils.enums import SectorType

"""
prediction data for black litterman
"""


class Prediction:
    def __init__(self, name: str, percentage: float, weights: Dict[SectorType, float]):
        self.name = name
        self.percentage = percentage
        self.weights = weights

    @classmethod
    def from_dict(cls, input_dict: Dict[str, Any]) -> Prediction:
        """
        constructor for model object from dict
        """

        name: str = input_dict['name']
        percentage: float = input_dict['percentage']
        weights: Dict[SectorType, float] = input_dict['weights']

        return cls(name, percentage, weights)
