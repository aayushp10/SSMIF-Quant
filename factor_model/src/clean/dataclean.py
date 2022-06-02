#!/usr/bin/env python3
"""
    Clean data
    The data is be cleaned and saved in clean_data/

    We will duplicate data for ease of use within subsequent models - this point is up for debate

    We will load valuation and sentiment-approximating data from a series of sector ETFs
    We will load macroeconomic data
"""

import pandas as pd
from sys import argv
from os.path import join, basename, splitext, exists

from loguru import logger
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Tuple, Union, cast, Optional, Dict
from scipy import signal

from classes.project import Project
from classes.bloomberg import BloombergData
from classes.base_data import BaseData
from classes.normalized_column import NormalizedColumn
from classes.additional import Additional

from utils.error_handling import HandleErrors
from utils.utils import normalize_str, load_dataframe_sanitize
from utils.enums import SectorType

from constants import raw_data_folder, date_key, non_numeric_cols, \
    clean_train_data_folder, clean_predict_data_folder, clean_data_file_name, \
    clean_daily_returns_file_name

from classes.global_config_data import GlobalConfigData
import re

REGEX_CHARS = re.compile('([ \-:])')


class CleanData:
    """
    This object will take in a project object and clean (interpolate) and 
    combine all of the data from bloomberg_data and additional into 
    one large data frame. 
    This will then both return the combined dataframe and save it to disk
    in a location determined from the project information. 
    the load_only_fs flag will signify whether or not you want to skip 
    the majority of the processing and just load saved clean data from disk and 
    return that instead
    """

    def __init__(self, project_name: str,
                 sector_type: SectorType,
                 bloomberg_data: Dict[str, BloombergData],
                 additional_data: Dict[str, Additional],
                 lag: int,
                 target: Optional[NormalizedColumn],
                 global_config: GlobalConfigData,
                 override_basename: Optional[str] = None,
                 load_only_fs: bool = False,
                 predict_data: bool = False) -> None:

        # self.tickername = list(bloomberg_data.keys())[0]
        # basename is the path basename for saving out the clean data
        self.basename = override_basename if override_basename is not None else self._get_basename(
            project_name, sector_type, global_config)
        # predict data shows if the data is in the predict data folder
        self.predict_data = predict_data
        # load_only_fs: if you ran dataclean already and you don't want to run it again, pass in True
        self.data, self.daily_returns, self.lagged_data = self._get_clean_data(
            bloomberg_data, additional_data, lag, target, global_config, load_only_fs)
        self.target = target
        self.lag = lag

    def _get_basename(self, project_name: str, sector_type: SectorType, global_config: GlobalConfigData) -> str:
        """
        get file basename (unique to clean data input)
        """
        file_name = REGEX_CHARS.sub('_', '_'.join([project_name, sector_type.name, str(
            global_config.window.start_date), str(global_config.window.end_date)]))
        return f'{file_name}.csv'

    def _get_clean_base_folder(self) -> str:
        return clean_predict_data_folder if self.predict_data else clean_train_data_folder

    def get_file_path(self) -> str:
        # this will return the file path that the data is being saved out to
        return join(self._get_clean_base_folder(),  f'{clean_data_file_name}_{self.basename}')

    def get_file_path_daily_returns(self) -> str:
        return join(self._get_clean_base_folder(), f'{clean_daily_returns_file_name}_{self.basename}')

    def extrapolate_to_date(self, end_date: datetime) -> None:
        # TODO - use end_date to extrapolate up to that date
        pass

    @staticmethod
    def _extrapolate_data(data: BaseData) -> pd.DataFrame:
        """
        extrapolate dates in dataframe, to lowest, iterative value
        """
        name, df = data.name, data.data
        logger.info(f"post-processing extrapolation for {name}")
        last_date: Union[datetime, None] = None
        last_row_numeric: List[float] = []
        numeric_indexes: List[int] = [x for x, col in enumerate(
            df.columns) if col not in non_numeric_cols]

        # for every row in the input raw data
        for _, row in df.iterrows():
            date = row.name
            # If the column contains numeric data (as defined by the list numeric_indexes) then save it into "current row numeric"
            current_row_numeric: List[float] = [
                val for x, val in enumerate(row.values) if x in numeric_indexes]
            # If the last date is not none and we have valid numeric data
            if last_date is not None and len(last_row_numeric) > 0:
                # get the change in date since the last piece of valid data
                delta_date = date - last_date
                num_days_between = delta_date.days - 1
                # Find all date gaps and keep track of the starting and ending values of the data along with the number of days in between
                if num_days_between >= 1:
                    deltas: List[float] = []
                    for j, curr_val in enumerate(current_row_numeric):
                        prev_val: float = last_row_numeric[j]
                        delta_val = curr_val - prev_val
                        delta_val_over_days = delta_val / \
                            (num_days_between + 1)
                        deltas.append(delta_val_over_days)

                    # Using the information from the last step, calculate the new numbers and insert them into the dataframe
                    current_day = last_date
                    for k in range(num_days_between):
                        numeric_data: List[float] = []
                        day_delta = k + 1
                        for l, delta in enumerate(deltas):
                            current_delta = delta * day_delta
                            numeric_data.append(
                                current_delta + last_row_numeric[l])
                        current_day = last_date + timedelta(days=day_delta)
                        df.loc[current_day] = numeric_data
            last_date = date
            last_row_numeric = current_row_numeric

        # Now that you have formal dates, use the builtin pandas methods to close everything out
        df = df.sort_index()
        # Interpolate missing values
        df = df.interpolate(method="linear", limit_direction="both")
        return df

    @staticmethod
    def _concat_list_data(concat_data: List[BaseData]) -> pd.DataFrame:
        """
        contcatenate two or more data frames from a list of dataframes
        """
        if len(concat_data) == 0:
            raise ValueError('cannot concat empty list')
        if len(concat_data) == 1:
            return concat_data[0].data

        logger.info("start concat dataframes")

        clean_concat_data: List[BaseData] = []

        not_renamed_cols = [date_key]

        # for each BaseData element in concat_data (ex BloombergData)
        for concat_element in concat_data:
            if len(concat_element.data) == 0:
                continue
            # sort by date and then store them back into the same frame
            concat_element.data = concat_element.data.sort_index()
            rename_columns: Dict[str, str] = {}
            for concat_col_name in concat_element.data.columns:
                if concat_col_name in not_renamed_cols:
                    continue
                # Create a normalized column (updated name and data source attribute)
                # None for empty cell, 0. for defaulting to zero
                normalized_col = NormalizedColumn(
                    concat_element.data_source_type, concat_element.name, concat_col_name)
                # Append the new normalized column names to the list of column names
                rename_columns[concat_col_name] = normalized_col.normalize_colname()

            concat_element.data = concat_element.data.rename(
                columns=rename_columns)
            # add this sorted by date BaseData element to clean_concat_data
            clean_concat_data.append(concat_element)

        # delete the old unsorted list of BaseData because clean_concat_data contains the sorted version
        # of what was in concat_data
        del concat_data
        new_df = pd.concat(
            [concat_element.data for concat_element in clean_concat_data], axis=1)
        output = CleanData.fill_ending_na(new_df)
        del clean_concat_data

        logger.success("done with all concats")
        return output

    @staticmethod
    def get_daily_returns(dataframe):
        """
        Get the daily returns of each column in the dataframe - transformation to percent change with
        same structure as the original df
        """
        output = dataframe.pct_change()
        output = output.fillna(0)
        return output

    @staticmethod
    def fill_ending_na(dataframe) -> pd.DataFrame:
        """
        If there are na values at the end of a dataframe then you need to fill them in with a linear interpolation
        or average value if that is too crazy
        """
        df = pd.DataFrame(data=dataframe)
        df_last = df.iloc[[-1, ]]
        check_for_nan = df_last.isnull().values.any()
        if check_for_nan == True:
            interpolated_df = df.interpolate(method='linear')
            return interpolated_df
        else:
            return df

    @staticmethod
    def lag_dataframe(dataframe: pd.DataFrame, static_columns: List[str], num_days: int) -> pd.DataFrame:
        """
        lag a dataframe by number of days
        """
        lagged_data = dataframe.copy()
        # adds in num_days rows at end
        for _ in range(num_days):
            lagged_data = lagged_data.append(
                pd.Series(name=lagged_data.index[-1] + timedelta(days=1)))

        # columns to lag
        changed_columns = [
            col for col in dataframe.columns if col not in static_columns]
        lagged_data_without_static = lagged_data[changed_columns]
        static_data = lagged_data[static_columns]
        lagged_data_without_static = lagged_data_without_static.shift(30)
        lagged_data_final = pd.concat(
            [lagged_data_without_static, static_data], axis=1)
        return lagged_data_final

        # lagged_data = pd.concat(lagged_data)

        # first_month_dates = lagged_data.iloc[0:num_days+1].index
        # lagged_data = lagged_data.iloc[num_days:]
        # for d in first_month_dates:
        #     lagged_data.insert(loc=d, )
        # for current_date, row in lagged_data.iterrows():
        #     old_date = current_date - timedelta(days=num_days)
        #     for col in changed_columns:
        #         lagged_data.loc[current_date][col] = dataframe.loc[old_date][col]

    # @staticmethod
    # def cross_correlation_lag(self, dataframe: pd.Dataframe, static_columns: List[str]) -> pd.Dataframe:
    #     cross_correlations: Dict = {}
    #     for col in dataframe.columns if col not in static_columns:
    #         ccf = signal.correlate(dataframe[static_columns[0]], dateframe[col])
    #         lags = signal.correlation_lags(len(dataframe[static_columns[0]],len(dateframe[col])))
    #         cross_correlation[col] = ccf
    #     return cross_correlation, lags

    def _get_clean_data(self, bloomberg_data: Dict[str, BloombergData], additional_data: Dict[str, Additional],
                        lag: int, target: NormalizedColumn, global_config: GlobalConfigData, load_only_fs: bool) -> Tuple[pd.DataFrame, pd.DataFrame, Optional[pd.DataFrame]]:
        """
        given data, clean and concatenate all of the dataframes,
        save the file and return a large dataframe
        """
        # Get the filepath generated from the basepath
        file_path = self.get_file_path()
        daily_returns_path = self.get_file_path_daily_returns()
        # if we want to use cached clean data
        if load_only_fs:
            # but we don't have any cached clean data...
            if not exists(file_path):
                raise ValueError(f'could not find file {file_path}')
            # and we do have cached clean data, then load it in and coerce the date column to be
            # a series of datetime objects and the numeric columns to be of a uniform type
            all_data_concat = load_dataframe_sanitize(
                file_path).loc[global_config.window.start_date: global_config.window.end_date + timedelta(days=1)]
            if lag != 0:
                lagged_data = self.lag_dataframe(
                    all_data_concat, [target.normalize_colname()], lag)
            else:
                lagged_data = None
            return all_data_concat, load_dataframe_sanitize(daily_returns_path), lagged_data

        if len(bloomberg_data.keys()) == 0 and len(additional_data.keys()) == 0:
            raise ValueError('cannot find additional or bloomberg data')

        # for all of the data saved in the bloomberg section of the project object being cleaned
        # Note, we are going through a dictionary which is why we are using .values to get the
        # BloombergData objects    bloomberg_data: Dict[str, BloombergData] = ...
        all_data: List[BaseData] = []
        for bloomberg_data in bloomberg_data.values():
            # explicitely cast the objects to type BloombergData for autocomplete to work well
            # as of the time of writing
            bloomberg_data_cast: BloombergData = cast(
                BloombergData, bloomberg_data)
            # call the extrapolate data function which actually interpolates missing data
            # and fills in the gaps between value reporing via linear interpolation
            bloomberg_data_cast.data = self._extrapolate_data(
                bloomberg_data_cast)
            # save the newly interpolated data
            all_data.append(bloomberg_data_cast)

        # for all of the data saved in the project's additional data
        # this will be an empty list if there is no additional data
        # because we use .get(data, []) in read_config
        for additional_data in additional_data.values():
            # explicitely typecast to additional data so autocomplete works as
            # expected as of the time of writing
            additional_data_cast: Additional = cast(
                Additional, additional_data)
            # call our interpolation and cleaning function
            additional_data_cast.data = self._extrapolate_data(
                additional_data_cast)
            # save it to the output list
            all_data.append(additional_data_cast)

        # concatenate all of the cleaned dataframes into one larger
        # dataframe (note: columns from non_concat_cols) will not
        # be concatenated together, however, the date column will be set
        # to encapsulate all input data
        all_data_concat = self._concat_list_data(
            all_data).loc[global_config.window.start_date: global_config.window.end_date + timedelta(days=1)]

        # TODO - create lag in dataframe, remove all rows with no data
        # dataframe, date is the same, dependent variables are 30 days in the past
        #lagged_data = all_data_concat.copy()
        # for _ in range(30):
        #    # lagged_data[lagged_data.iloc[-1] + timedelta(days=1)] = lagged_data[lagged_data.iloc[-1]]
        #    lagged_data.append(pd.Series(name=lagged_data.index[-1] + timedelta(days=1)))

        # target_df = all_data_concat[[target.normalize_colname()]]
        # lagged_data = all_data_concat.drop(columns=[target.normalize_colname()])
        # lagged_data = all_data_concat.shift(30)
        # # lagged_data.concat(target_df)
        # lagged_data = pd.concat([lagged_data, target_df])

        # # start_date = all_data_concat.iloc[30]
        # print("===========before=============")
        # print(all_data_concat)
        if lag != 0:
            lagged_data = self.lag_dataframe(
                all_data_concat, [target.normalize_colname()], lag)
        else:
            lagged_data = None
        # print("===========after=============")
        # print(lagged_data)
        # all_data_concat = lagged_data

        # TODO - we probably need to save the data for the days lost due to lagging the data.
        # should we create 2 dataframes, 1 with all the data, and 1 with the lagged data, and
        # use the lagged data for training, and the data that was not lagged for predicting?
        # i guess when we create a "predict" dataframe we can rectify the issues with the dates
        # to make it consistent with the lagged data dates

        daily_returns = self.get_daily_returns(all_data_concat)
        # save the new dataframe to csv at file_path
        # which was retrieved from self.get_file_path

        # print(file_path)
        all_data_concat.to_csv(file_path)
        # exit()
        daily_returns.to_csv(daily_returns_path)
        # return the concatenated data as well
        return all_data_concat, daily_returns, lagged_data
