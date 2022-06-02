#!/usr/bin/env python3
"""
Predict file
"""
# Import necessary packages
from __future__ import annotations

from typing import Dict, Any, List

from classes.normalized_column import NormalizedColumn
from classes.window import Window
from classes.bloomberg import BloombergData
from classes.additional import Additional
from utils.enums import SectorType


class PredictData:
    """
    Predict Data Object
    """

    def __init__(self, same_as_train: bool, bloomberg: Dict[str, BloombergData], additional: List[Additional]) -> None:
        self.same_as_train = same_as_train
        self.bloomberg = bloomberg
        self.additional = additional

    @classmethod
    def from_dict(cls, input_data: Dict[str, str]) -> PredictData:
        """
        constructor for predict data from dict
        """
        same_as_train_key = 'same_as_train'
        bloomberg_data_key = 'bloomberg'
        same_as_train = input_data[same_as_train_key]
        bloomberg_data: Dict[str, BloombergData] = {}
        for tickername, raw_bloomberg_config in input_data.get(bloomberg_data_key, {}).items():
            current_bloomberg_data = BloombergData.from_dict(new_project, tickername,
                                                             raw_bloomberg_config, args.bloomberg)
            bloomberg_data[tickername] = current_bloomberg_data

        additional_data_key = 'additional'
        additional_data: List[Additional] = []
        for additional_name, raw_additional_config in input_data.get(additional_data_key, {}).items():
            current_additional_data = Additional.from_dict(new_project, additional_name,
                                                           raw_additional_config, args.additional)
            additional_data.append(current_additional_data)

        return cls(same_as_train, bloomberg_data, additional_data)


class Predict:
    """
    Predict object for saving prediction data
    """
    # Initialize parameters for Predict class

    def __init__(self, data: PredictData, target: NormalizedColumn, window_size: int, output_window: Window) -> None:
        self.data = data
        self.target = target
        self.window_size = window_size
        self.output_window = output_window

    @classmethod
    def from_dict(cls, sector_type: SectorType, input_dict: Dict[str, str]) -> Window:
        """
        constructor for prediction from dict
        """
        # keys
        data_key = 'data'
        target_key = 'target'
        window_size_key = 'window_size'
        output_window_key = 'output_window'

        data = PredictData.from_dict(input_dict[data_key])
        target = NormalizedColumn.from_dict(
            sector_type, input_dict[target_key])
        window_size = input_dict[window_size_key]
        output_window = Window.from_dict(input_dict[output_window_key])

        return cls(data, target, window_size, output_window)
