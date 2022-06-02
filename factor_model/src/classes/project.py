#!/usr/bin/env python3
"""
Project Encapsulation
"""
from typing import Dict
from .window import Window
from .global_config_data import GlobalConfigData
from utils.enums import SectorType, OptimizerType
from predict.optimizer import Optimizer


class Project(GlobalConfigData):
    """
    Project encapsulation
    """
    # Initialize parameters for Project class

    def __init__(self, project_name: str, window: Window, rebalance_period: int):
        super().__init__(project_name, window)
        self.name = project_name
        self.sectors: Dict[SectorType, Sector] = {}
        self.optimizations: Dict[OptimizeTyper, BaseOptimization] = {}
        self.rebalance_period = rebalance_period
