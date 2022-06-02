---
id: data-cleaning
title: Data Cleaning
sidebar_label: Data Cleaning
slug: /data-cleaning
---
### Developers
- [Michael DiGregorio](https://www.linkedin.com/in/michael-jonathan-digregorio/)
- [Agatha Malinowski](https://www.linkedin.com/in/agatha-malinowski-1a2298179/)

## What does data cleaning do?

- Data cleaning is comprised of extrapolation and data formatting. All dataframes are concatenated into a single large dataframe, with many columns used to link to the original data source. The index is set to a datetime object, and any fields that are empty are filled in.

## How it All Works

- All data objects are stored within its self. These objects are a string name, two dictionaries of strings bloomberg_data and additonal_data, override_basename, and two boolean values load_only_fs and predict_data. Below is the constructor for data being selected.
```python
def __init__(self, name: str,
                bloomberg_data: Dict[str, BloombergData],
                additional_data: Dict[str, Additional],
                override_basename: Optional[str] = None,
                load_only_fs: bool = False,
                predict_data: bool = False) -> None:
    # basename is the path basename for saving out the clean data 
    self.basename = override_basename if override_basename is not None \
        else f"{name}.csv"
    # predict data shows if the data is in the predict data folder
    self.predict_data = predict_data
    # load_only_fs: if you ran dataclean already and you don't want to run it again, pass in True
    self.data, self.daily_returns = self._get_clean_data(bloomberg_data, additional_data, load_only_fs)


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
```

- The get_clean_data() function will take in the data, clean the data, concatenate the data, and save the file returning a large dataframe. This is the method that calls all the methods listed below. Using he data pulled in through self, the data can be extrapolated, concatenated, used to calculate the percentage change in daily returns, and interpolated over to fill in any nan values.

```python
def _get_clean_data(self, bloomberg_data: Dict[str, BloombergData], additional_data: Dict[str, Additional], load_only_fs: bool) -> pd.DataFrame:
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
        return load_dataframe_sanitize(file_path), load_dataframe_sanitize(daily_returns_path)

    if len(bloomberg_data.keys()) == 0 and len(additional_data) == 0:
        raise ValueError('cannot find additional or bloomberg data')

    # for all of the data saved in the bloomberg section of the project object being cleaned
    # Note, we are going through a dictionary which is why we are using .values to get the 
    # BloombergData objects    bloomberg_data: Dict[str, BloombergData] = ...
    all_data: List[BaseData] = []
    for bloomberg_data in bloomberg_data.values():
        # explicitely cast the objects to type BloombergData for autocomplete to work well
        # as of the time of writing
        bloomberg_data_cast: BloombergData = cast(BloombergData, bloomberg_data)
        # call the extrapolate data function which actually interpolates missing data
        # and fills in the gaps between value reporing via linear interpolation
        bloomberg_data_cast.data = self._extrapolate_data(bloomberg_data_cast)
        # save the newly interpolated data
        all_data.append(bloomberg_data_cast)

    # for all of the data saved in the project's additional data 
    # this will be an empty list if there is no additional data
    # because we use .get(data, []) in read_config
    for additional_data in additional_data:
        # explicitely typecast to additional data so autocomplete works as 
        # expected as of the time of writing
        additional_data_cast: Additional = cast(Additional, additional_data)
        # call our interpolation and cleaning function
        additional_data_cast.data = self._extrapolate_data(additional_data_cast)
        # save it to the output list
        all_data.append(additional_data_cast)

    # concatenate all of the cleaned dataframes into one larger
    # dataframe (note: columns from non_concat_cols) will not 
    # be concatenated together, however, the date column will be set
    # to encapsulate all input data
    all_data_concat = self._concat_list_data(all_data)

    daily_returns = self.get_daily_returns(all_data_concat)
    # save the new dataframe to csv at file_path 
    # which was retrieved from self.get_file_path
    
    all_data_concat.to_csv(file_path)
    daily_returns.to_csv(daily_returns_path)
    # return the concatenated data as well
    return all_data_concat, daily_returns
```

- After the data is selected, it is time for the data to be read and cleaned. In order to begin, we consider the following methods.
```python
def _extrapolate_data(data: BaseData) -> pd.DataFrame:
    """
    extrapolate dates in dataframe, to lowest, iterative value
    """
def _concat_list_data(concat_data: List[BaseData]) -> pd.DataFrame:
    """
    contcatenate two or more data frames from a list of dataframes
    """
def get_daily_returns(dataframe):
    """
    Get the daily returns of each column in the dataframe - transformation to percent change with
    same structure as the original df
    """
def fill_ending_na(dataframe):
    """
    If there are na values at the end of a dataframe then you need to fill them in with a linear interpolation
    or average value if that is too crazy
    """
```

## _extrapolate_data(data: BaseData)

- Extrapolate data reads the data and fixes date gaps. It does this by keeping track of starting and ending values of the data in addition to the number of days between. It then calculates new numbers and inserts them into the dataframe. Once the dates are formalized, nan data will be interpolated on using a linear interpolation. The code is as follows:
```python
@staticmethod
def _extrapolate_data(data: BaseData) -> pd.DataFrame:
    """
    extrapolate dates in dataframe, to lowest, iterative value
    """
    name, df = data.name, data.data
    logger.info(f"post-processing extrapolation for {name}")
    last_date: Union[datetime, None] = None
    last_row_numeric: List[float] = []
    numeric_indexes: List[int] = [x for x, col in enumerate(df.columns) if col not in non_numeric_cols]

    # for every row in the input raw data
    for _, row in df.iterrows():
        date = row.name
        # If the column contains numeric data (as defined by the list numeric_indexes) then save it into "current row numeric"
        current_row_numeric: List[float] = [val for x, val in enumerate(row.values) if x in numeric_indexes]
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
                    delta_val_over_days = delta_val / (num_days_between + 1)
                    deltas.append(delta_val_over_days)

                # Using the information from the last step, calculate the new numbers and insert them into the dataframe
                current_day = last_date
                for k in range(num_days_between):
                    numeric_data: List[float] = []
                    day_delta = k + 1
                    for l, delta in enumerate(deltas):
                        current_delta = delta * day_delta
                        numeric_data.append(current_delta + last_row_numeric[l])
                    current_day = last_date + timedelta(days = day_delta)
                    df.loc[current_day] = numeric_data
        last_date = date
        last_row_numeric = current_row_numeric

    # Now that you have formal dates, use the builtin pandas methods to close everything out
    df = df.sort_index()
    # Interpolate missing values
    df = df.interpolate(method="linear", limit_direction="both")
    return df
```

## _concat_list_data(concat_data: List[BaseData])

- The concat_list_data() method concatinates two or more dataframes together from a list of dataframes. It does this by sorting by date and storing them back into the same frame. It then creates a new normalized column where the updated names and dates will be stored and appends it back to the list of column names.
```python
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
            normalized_col = NormalizedColumn(concat_element.data_source_type, concat_element.name, concat_col_name)
            # Append the new normalized column names to the list of column names 
            rename_columns[concat_col_name] = normalized_col.normalize_colname()

        concat_element.data = concat_element.data.rename(columns=rename_columns)
        # add this sorted by date BaseData element to clean_concat_data
        clean_concat_data.append(concat_element)


    # delete the old unsorted list of BaseData because clean_concat_data contains the sorted version
    # of what was in concat_data
    del concat_data
    new_df = pd.concat([concat_element.data for concat_element in clean_concat_data], axis=1)
    output = CleanData.fill_ending_na(new_df)
    del clean_concat_data

    logger.success("done with all concats")
    return output
```
## get_daily_returns(dataframe)

- Calculates the daily returns of each column in the dataframe. The daily returns are recorded as percentage change.

```python
@staticmethod
def get_daily_returns(dataframe):
    """
    Get the daily returns of each column in the dataframe - transformation to percent change with
    same structure as the original df
    """
    output = dataframe.pct_change()
    output = output.fillna(0)
    return output
```

## fill_ending_na(dataframe)

- Sometimes the data has nan values at the end of the dataframe. The model will not work unless this data is filled. The fill_ending_na() method will fill in the missing data with a linear interpolation of the data.
```python
@staticmethod
def fill_ending_na(dataframe):
    """
    If there are na values at the end of a dataframe then you need to fill them in with a linear interpolation
    or average value if that is too crazy
    """
    df = pd.DataFrame(data=dataframe)
    df_last = df.iloc[[-1,]]
    check_for_nan = df_last.isnull().values.any()
    if check_for_nan == True:
        interpolated_df = df.interpolate(method = 'linear')
        return interpolated_df
    else:
        return df
```


