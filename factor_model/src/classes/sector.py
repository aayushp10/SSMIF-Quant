#!/usr/bin/env python3
"""
Sector Encapsulation
"""
from typing import Dict, List

from .bloomberg import BloombergData
from .additional import Additional
from .model import Model
from .operation import Operation
from .predict import Predict
from utils.enums import SectorType


class Sector:
    """
    Sector encapsulation
    """

    def __init__(self, sector: SectorType, lag: int, predict: Predict):
        self.sector = sector
        self.lag = lag
        self.bloomberg_data: Dict[str, BloombergData] = {}
        self.additional_data: Dict[str, Additional] = {}
        self.operations: List[Operation] = []
        self.models: List[Model] = []
        self.predict: Predict = predict
