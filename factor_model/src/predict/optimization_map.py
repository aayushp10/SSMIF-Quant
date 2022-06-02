#!/usr/bin/env python3
"""
Optimize type map
"""
from predict.optimizer import Optimizer
from predict.black_litterman import BlackLitterman
from predict.hrp import HRP
from utils.enums import OptimizerType
from typing import Dict, List

optimizer_type_map: Dict[OptimizerType, Optimizer] = {
    OptimizerType.black_litterman: BlackLitterman,
    OptimizerType.hrp: HRP
}
