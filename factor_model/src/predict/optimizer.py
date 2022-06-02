#!/usr/bin/env python3
"""
optimizer
"""
from abc import ABCMeta, abstractmethod
from typing import Dict, Any, List, Tuple
from utils.enums import SectorType
from classes.normalized_column import NormalizedColumn
from classes.bloomberg import BloombergData


class Optimizer(metaclass=ABCMeta):
    def __init__(self, hyperparams: Dict[str, Any], benchmark: Dict[str, BloombergData]):
        self.hyperparams = hyperparams
        self.benchmark = benchmark

    @property
    @abstractmethod
    def optimizer_type(self):
        """
        The type of the given optimizer
        OptimizerType enum
        """
        pass

    @property
    @abstractmethod
    def weights(self):
        """
        The weights
        Dict[SectorType, float]
        """
        pass

    @abstractmethod
    def run_optimization(self, predictions: Dict[SectorType, List[float]], sector_data: Dict[SectorType, Tuple[Any, NormalizedColumn]]) -> None:
        """
        function that runs the optimization

        sector_data is Dict[SectorType, Tuple[CleanData, NormalizedColumn]]
        """
        pass

    @abstractmethod
    def scale_weights(self, weights: Dict[SectorType, float]) -> Dict[SectorType, float]:
        """
        function that scales the weights of the allocations between a given constraint
        """
        pass
