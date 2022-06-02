#!/usr/bin/env python3
"""
Base Learn Model
"""

from os.path import join
from classes.model import Model
from utils.enums import ModelType, SectorType
from typing import List, Dict, Optional, Any
import pickle
from constants import models_folder
from utils.utils import relative_file_path
from classes.window import Window
import re

REGEX_CHARS = re.compile('([ \-:])')


class BaseModel(Model):

    uses_window: bool = False

    def __init__(self, name: str, sector_type: SectorType,
                 predictors: List[Dict[str, str]],
                 hyper_parameters: Dict[str, Any],
                 fit_parameters: Dict[str, Any],
                 training_window: Window):

        super().__init__(name, sector_type, predictors,
                         hyper_parameters, fit_parameters, training_window)

    @property
    def saved_model_path(self) -> str:
        """
        load models from disk
        """
        base_name = REGEX_CHARS.sub('_', '_'.join([self.name, self.model_type.name, str(
            self.training_window.start_date), str(self.training_window.end_date)])) + '.pkl'
        file_path = relative_file_path(join(models_folder, base_name))
        return file_path

    def save_model(self) -> None:
        """
        save models to disk
        """
        with open(self.saved_model_path, 'wb') as save_model_file:
            pickle.dump((self.model, self.error), save_model_file)

    def load_model(self) -> None:
        """
        load model from disk
        """
        with open(self.saved_model_path, 'rb') as save_model_file:
            self.model, self.error = pickle.load(save_model_file)
