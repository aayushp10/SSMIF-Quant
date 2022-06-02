---
id: loading-bloomberg-data
title: Loading Bloomberg Data
sidebar_label: Loading Bloomberg Data
slug: /loading-bloomberg-data
---
### Developers
- [Michael DiGregorio](https://www.linkedin.com/in/michael-jonathan-digregorio/)

### How to Load With The Config
- Refer to [here](the-config-file/#bloomberg) for information on how to load with the config. This will be a technical guide on how the code behind that functionality works

### How This Guide Will Flow
- [bloombergtest.py](#bloomberg-test)
- [main.py](#where-the-function-call-starts)
- [read_config.py](#read-config)
- [base_data.py](#base-data)
- [bloomberg.py](#bloomberg)

### Validating That Bloomberg Is Correctly Installed
- To validate that the Bloomberg API is correctly installed on your machine, please make sure that you have completed the following steps [source](https://medium.com/@johann_78792/getting-started-with-bloombergs-python-desktop-api-5fd083b4193a)

If the link is invalid, please see this copy of the content [here](how-to-install-bloomberg)

### Bloomberg Test
- Run the script "bloombergtest.py" and check to make sure that you are getting valid output dataframes. Please validate that the data fields being loaded are still valid. The content of that file is preserved below:
```python
import pdblp
import pandas as pd

def main():
    con = pdblp.BCon(timeout=10000)
    con.start()
    frame = con.bdh(['FB US Equity'], ["PX_LAST"], start_date="20200101", end_date="20200303")
    print(frame)

if __name__ == "__main__":
    main()
```

:::warning

Note that if pdblp becomes non-functional, you will have to rewrite data loading code to take advantage of whatever framework is contemporary

:::

- If you get a valid dataframe printed then congratulations! Your Bloomberg install works. <b>If you are having trouble please call Bloomberg directly and explain that you are a Stevens student who wants to gain access to "Bloomberg Anywhere" and the "Bloomberg Desktop API"</b>

### Where The Function Call Starts
- The dataload function call starts in main.py when we call "read_config" like this: 
```python 
    projects, optimization_data = read_config(args)
```
- Where "args" are the command line arguments parsed by the argparse package, which are defined and initialized by these lines:
```python 
    parser = argparse.ArgumentParser(description="SSMIF Factor Model")

    parser.add_argument("-b", "--bloomberg", default=False, action="store_true", help="load bloomberg data from filesystem")
    parser.add_argument("-a", "--additional", default=False, action="store_true", help="load additional data from filesystem")
    parser.add_argument("-o", "--operations", default=False, action="store_true", help="load additional data from operations")
    parser.add_argument("-v", "--viz", default=False, action="store_true", help="run data visualization")
    parser.add_argument("-c", "--clean", default=False, action="store_true", help="load cleaned data from filesystem")
    parser.add_argument("-t", "--train", default=False, action="store_true", help="load training output from filesystem")
    parser.add_argument("-p", "--portfolio-optimziation", default=True, action="store_true", help="skip portfolio optimization")
    parser.add_argument("-r", "--predict", default=False, action="store_true", help="skip run predictions")
    parser.add_argument("--black-litterman", default=False, action="store_true", help="compute the optimized portfolio using the black litterman model")
    parser.add_argument("--hrp", default=False, action="store_true", help="compute the optimized portfolio using a hierarchical risk parity model")
    parser.add_argument("config", type=str, help="path to config file from config folder")

    args = parser.parse_args()
```
- Note that all of the options regarding bloomberg, additonal, operations, viz, clean, and train are opt-out, i.e if you call the main function with those flags it will check your filesystem for existing output and <b>NOT</b> rerun those model sections to save you time if you are debugging / experimenting

- By calling that function we run all of the appropriate content of read_config.py, which initalizes our dataloading pipeline

### Read Config
- We intialize our BloombergData objects in read_config using the following lines:
```python
    # create bloombergdata object that contains the loaded data (from Bloomberg API or from disk) and then store it in the project
    for tickername, raw_bloomberg_config in input_data.get(bloomberg_data_key, {}).items():
        current_bloomberg_data = BloombergData.from_dict(new_project, tickername, 
                                                            raw_bloomberg_config, args.bloomberg)
        new_project.bloomberg_data[tickername] = current_bloomberg_data
```
- This is nested within a forloop of all of the projects in config_data.items()
- What we are dong is that for every project outlined in the config data, initialize a new array of BloombergData objects within every project that corresponds to the bloomberg data that you want to load for that project. Thats why you see "new_project.bloomberg_data[tickername] = current_bloomberg_data" for "new_project," which is the current project we have reached via iteration, add an array of BloombergData objects which correspond to the data we have specified in the config file. One BloombergData object per "ticker" loaded

- For example, this segment of the config file would produce two BloombergData objects within the project they are a part of:
```yaml
      S5FINL Index:
        output_basename: NULL
        cols: 
          - PX_LAST
          - PE_RATIO
          - PX_TO_BOOK_RATIO
          - PX_TO_SALES_RATIO
          - FREE_CASH_FLOW_YIELD
          - EST_LTG_EPS_AGGTE
          - TOT_DEBT_TO_TOT_ASSET
          - EARN_YLD
          - PUT_CALL_OPEN_INTEREST_RATIO
          - EQY_INST_PCT_SH_OUT
          - PX_VOLUME
        col_map: []

      S5ENRS Index:
        output_basename: NULL
        cols: 
          - PX_LAST
          - PE_RATIO
          - PX_TO_BOOK_RATIO
          - PX_TO_SALES_RATIO
          - FREE_CASH_FLOW_YIELD
          - EST_LTG_EPS_AGGTE
          - TOT_DEBT_TO_TOT_ASSET
          - EARN_YLD
          - PUT_CALL_OPEN_INTEREST_RATIO
          - EQY_INST_PCT_SH_OUT
          - PX_VOLUME
        col_map: []
```
- One BloombergData object stores information loaded from the S5FINL Index and one stores information on the S5ENRS Index

### Base Data
- BloombergData inherits from our BaseData class, found in src/classes/base_data.py
- The constructor is as follows, and is used to store filepath information, data information, and <b>calls the self._load_data() method</b>. Data is loaded when the constructor of the base class is called.
```python
  class BaseData(metaclass=ABCMeta):
      filename_split_char: str = '_'

      #Initialize parameters for the Base Data class
      def __init__(self, global_config: GlobalConfigData, name: str, columns: List[str],
                  col_map: List[Dict[str, str]], override_basename: Optional[str] = None,
                  load_only_fs: bool = False):
          self.name = name
          self.columns = columns
          self.col_map = col_map
          #generate a basename for the data: if one is provided, use that, otherwise, set the basename to the normalized name for the data
          self.basename = override_basename if override_basename is not None \
              else f"{normalize_str(self.name)}.csv"
          self.data = self._load_data(global_config, load_only_fs)
```

- You will notice that BaseData inherits from ABCMeta, this is an artifact of janky python implementations of abstract base classes. This, combined with the decorators you will see below, allows the compiler to check to make sure that all of the properties and abstract methods are successfully overridden. 

- As for the decorators, here is some important vocabulary:
  - @property refers to a variable that the child class must define. Properties must be defined outside of the constructor. For example, BloombergData defines the property "data_source_type" like so: 
```python
class BloombergData(BaseData):
    data_source_type = DataSource.bloomberg
    def __init__(self, global_config: GlobalConfigData,
```
- Notice how data_source_type is defined above the constructor. Importantly, this variable can be overridden in the constructor.

- @abstractmethod refers to anything that you want your child classes to implement. Becuase of janky python abstract base class implementations, everything has to be a method (including the properties), its just that properties also include the @property tag

- @staticmethod refers to any method which does not take "self" as an argument. This means that it does not have access to any of the "self" attributes of an object. You do this for functions that should be logically grouped within a class, but do not need access to any of its internal data. For more help with @staticmethod and @classmethod, check out [this page](staticmethods-classmethods)
 

- @HandleErrors is a SSMIF custom decorator which prints the location and stack-trace of an error in a slightly nicer format than default. It allows any function it decorates to gracefully error out without having to incude try : except blocks everywhere. 

- So, to fulfil the "contract" you sign by inherriting from base data, your class needs to define the following: 
  - The "data_source_type" property
  - The "_load_dataset()" method
- And your class gains access to the following functions from its parent:
  - "get_folder_path()"
  - "get_file_path()"
  - "load_data()" (this just calls _load_dataset with some extra pazzaz)

- The contract is defined by the following code:
```python 
  class BaseData(metaclass=ABCMeta):
      filename_split_char: str = '_'

      #Initialize parameters for the Base Data class
      def __init__(self, global_config: GlobalConfigData, name: str, columns: List[str],
                  col_map: List[Dict[str, str]], override_basename: Optional[str] = None,
                  load_only_fs: bool = False):
          self.name = name
          self.columns = columns
          self.col_map = col_map
          #generate a basename for the data: if one is provided, use that, otherwise, set the basename to the normalized name for the data
          self.basename = override_basename if override_basename is not None \
              else f"{normalize_str(self.name)}.csv"
          self.data = self._load_data(global_config, load_only_fs)


      @property
      @abstractmethod
      def data_source_type(self):
          """
          data source type
          """
          pass

      @staticmethod
      def get_folder_path(project_name: str) -> str:
          return relative_file_path(join(raw_data_folder, project_name))

      def get_file_path(self, folder_path: str) -> str:
          path_prepend = data_source_prepend_map[self.data_source_type]
          return join(folder_path, self.filename_split_char.join([path_prepend, self.basename]))

      @HandleErrors
      def _load_data(self, global_config: GlobalConfigData, load_only_fs: bool) -> pd.DataFrame:
          """
          whole point of this is to set the data property on obj
          """
          # get folder path for the project
          folder_path = self.get_folder_path(global_config.project)
          file_path = self.get_file_path(folder_path)

          # if you want to load from filesystem and the file does not exist: error
          # If you do not want to load the data from bloomberg API then use this
          # For additional, if you have the flag set that would imply that you
          # have run this or have the .csv file that you want so you want to load it
          # from wherever we auto save it. Otherwise if you run this we will go in
          # and save a copy of the cleaned version of your original csv so that later on
          # its stored here
          
          if load_only_fs:
              if not exists(file_path):
                  raise ValueError(f'could not find file {file_path}')
              return load_dataframe_sanitize(file_path)

          # Load the data
          data: pd.DataFrame = self._load_dataset(global_config)

          # Change the column names to match the col_map laid out in the config
          for col_map in self.col_map:
              data = map_columns(data, col_map)

          # If the folder that we are supposed to save this to does not exist, create it
          if not exists(folder_path):
              makedirs(folder_path, exist_ok=True)

          # Save the data
          logger.info(f'columns: {data.columns}')
          logger.info(f'saving data to {file_path}')
          data.to_csv(file_path)

          return data

      @abstractmethod
      def _load_dataset(self, global_config: GlobalConfigData):
          pass
```

### Bloomberg
 - This file contains the class for BloombergData, which inherits from the BaseData class, whose documentation can be found right above this.
 
 - Right before the constructor, you will find the following code which maps data source type to DataSource.bloomberg
 
 ```python
class BloombergData(BaseData):
    data_source_type = DataSource.bloomberg
  ```
 
 - The constructor of the class initializes the all of the parameters that are in BaseData, including global_config, tickername, columns, col_map, override_basename, and load_only_fs. This is done using super().__init__()
 
 ```python
  def __init__(self, global_config: GlobalConfigData,
                          tickername: str,
                          columns: List[str], 
                          col_map: List[Dict[str, str]],
                          override_basename: Optional[str] = None, 
                          load_only_fs: bool = False):
          # Data is loaded on creation of the bloomberg object and then stored in self.data
          # It is also saved to disk simultaneously
          super().__init__(global_config, tickername, columns, col_map, override_basename, load_only_fs)
 ```
 
 - @classmethod is a method that is referring to the class itself instead of a created object. To use this, it has to take in cls. This works similar to the way self works for a class object. For more help with @staticmethod and @classmethod, check out [this page](staticmethods-classmethods)
 
 - In this case, our method, from_dict, is a class method. It will take in cls, global_config, name, input_dict, and load_only_fs as parameters and will return a bloomberg data object. The code for this is as follows:
 
 ``` python
 @classmethod
    def from_dict(cls, global_config: GlobalConfigData, name: str, input_dict: Dict[str, Any], load_only_fs: bool) -> BloombergData:
        """
        constructor for bloomberg data from dict
        """
        return cls(global_config, name,
                   input_dict[columns_key],
                   input_dict.get(column_map_key, []),
                   input_dict.get(file_base_name_override_key),
                   load_only_fs)
 ```

 - _load_dataset_bloomberg is a method that specifies the data that we want to load from bloomberg itself. This format for fetching data from bloomberg is outlined in the blpapi documentation. To start, we have to change the start and end date that we have outlined in the config file to match that of Bloomberg's request services. This is done by using date_block_format, which will make the date take the form of yyyymmdd. The next line is connecting to the bloomberg API and getting the data we want based on the tickernames, columns, start date, and end date. The code is as follows:

 ``` python
 def _load_dataset_bloomberg(self, connection: pdblp.BCon, ticker_names: List[str], columns: List[str], global_config: GlobalConfigData) -> pd.DataFrame:
            """
            :param dataset_name: list of dataset names to be passed into the con object : List[str]
            :param cols: list of fields to pull for each dataset from the con object : List[str]
            :return: A dataframe containing the data from bloomberg
            """
            date_block_format: str = '%Y%m%d'
            df = connection.bdh(ticker_names, columns, global_config.window.start_date.strftime(
                date_block_format), global_config.window.end_date.strftime(date_block_format))

            df = self.fix_dataframe(df)

            return df
 ```

- As you can see, at the end of this, we have a @staticmethod called fix_dataframe. A static method is a method that can be called without an object of that class. When we initially pull bloomberg data. we are given a dataframe with three header rows. This method deletes those three rows, extracts the original column names, and resets the index to be the dates in order to present a clean and ordinarily shaped dataframe as one would expect.

```python
 @staticmethod
    def fix_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """
        dataframe with 3 header rows is converted to 1
        """
        new_columns: List[str] = df.columns.get_level_values(1).values
        dates = df.index
        df = pd.DataFrame(df.values, columns=new_columns)
        df[date_key] = dates
        df = df.set_index(date_key)

        return df
```

- Finally, we have our _load_dataset method which will try to establish a connection to bloomberg and load the dataset using the _load_dataset_bloomberg method discussed earlier. The code for this is also straight from the pdblp documentation and follows the format given by bloomberg. We used try and except in order to help identify common problems such as not having a connection with bloomberg running, or not having the correct module for pdblp installed. The code is below for your reference. 

```python
 def _load_dataset(self, global_config: GlobalConfigData) -> pd.DataFrame:
        # Attempt bloomberg connection
        try:
            import pdblp
        except ModuleNotFoundError:
            logger.error("Unable to find pdblp module. env error")

        try:
            connection = pdblp.BCon(timeout=30000)
            connection.start()
        except Exception as err:
            logger.error("Unable to establish connection with Bloomberg API")
            raise err

        # Load the data from bloomberg
        date_block_format: str = '%Y%m%d'

        data = self._load_dataset_bloomberg(connection, [self.name], self.columns, global_config)

        return data
```