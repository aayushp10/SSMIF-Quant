#!/usr/bin/env python3
"""
    This file will be a repository for a seres of 'constants' we will use throughout the Factor Model
    I haven't decided if this should be a python file, .yml file, or both
"""
from datetime import date
from typing import List
from os.path import join

# percentage of data used for training and testing
train_size: int = 0.8
test_size: int = 1-train_size

# number of days to leave between train and test sets
gap: int = 10

data_folder: str = "data"
raw_data_folder: str = join(data_folder, "raw_data")

# data/clean_data/<train|predict>/<data|daily_returns>

clean_data_folder: str = join(data_folder, "clean_data")
clean_train_data_folder: str = join(clean_data_folder, "train")
clean_predict_data_folder: str = join(clean_data_folder, "predict")
clean_data_file_name: str = "data"
clean_daily_returns_file_name: str = "daily_returns"

operated_data_folder: str = join(data_folder, "operated_data")
config_folder: str = "configs"
models_folder: str = "models"
data_viz_folder: str = "visualizations"
results_folder: str = "results"
weights_path: str = join(results_folder, "weights")
hrp_weights_path: str = join(results_folder, "hrp_weights.csv")
date_format: str = "%Y-%m-%d"

date_key: str = 'date'
non_numeric_cols: List[str] = [date_key]


holidays: List[date] = [date(1994, 4, 27), date(2001, 9, 11), date(2001, 9, 14), date(2004, 6, 11),
                        date(2007, 1, 2), date(2012, 10, 29), date(2012, 10, 30), date(2018, 12, 5)]


# global keys for config
columns_key = 'cols'
file_base_name_override_key = 'output_basename'
column_map_key = 'col_map'
