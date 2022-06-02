---
id: operations-functions
title: How Operations Functions Work
sidebar_label: How Operations Functions Work
slug: /operations-functions
---
### Developers
- [Michael DiGregorio](https://www.linkedin.com/in/michael-jonathan-digregorio/)

## Where is Everything?
Up first, everything you need to modify the operations in the Factor Model is contained in the <b>FactorModel > src > operations</b> directory

- In that directory you should find two files, operations_fucntions.py and run_operations.py

#### Note: Every operation in the Factor Model is just a python function that takes in a dataframe and a set of extra keyword arguments as input parameters, and then returns a tuple of Pandas Series objects (if you just want to return one pandas series then you can just do this:  " return series_name, " )

## If You Just Want to Add Some New Functions
- Open up the file "operations_functions" 
- Up on top, you should see our import statements, followed by a series of python function definitions
- At the very bottom of the file you will see an enum object called "FunctionType" which inherits from class "BaseEnum," and a dictionary called "function_map" of type "Dict[FunctionType, Callable]"
- To add a new function, you write a new python function that takes a pandas dataframe and optionally a set of keyword arguments as an input, and then returns a tuple of Iterables. To only return one series then your return statement should look like " return series_name, " i.e you're returning tuple(pd.Series, None) 

### Example
Lets say that FunctionType and function_map look like this when we start
```python
class FunctionType(BaseEnum):
    """
    Enum to store valid function types
    """
    take_ratio = 'take_ratio'
    lag_column = 'lag_column'


function_map: Dict[FunctionType, Callable] = {
    FunctionType.take_ratio: take_ratio,
    FunctionType.lag_column: lag_column,
}
```

Now lets say that we write a new function called "scale_by" which takes in a column and scales it by the input number, and can take in a fill_value, which is the value you would fill Nan's with. The function would look like this: 
```python
def scale_by(data: pd.DataFrame, scale: float=None, fill_value: Optional[float]=None) -> Tuple[Iterable]:
    if scale == None:
        raise ValueError("Need to input a 'scale' argument to the operation defined by 'scale_by'")

    output_column: pd.Series = data[data.columns[0]].multiply(scale, fill_value=fill_value)

    return output_column, 
```

We would change FunctionType and function_map to look like this: 
```python 
class FunctionType(BaseEnum):
    """
    Enum to store valid function types
    """
    take_ratio = 'take_ratio'
    lag_column = 'lag_column'
    scale_column = 'scale_column'


function_map: Dict[FunctionType, Callable] = {
    FunctionType.take_ratio: take_ratio,
    FunctionType.lag_column: lag_column,
    FunctionType.scale_column: scale_by
}
```
#### Note: I refer to the functionality we just wrote as "scale_column" to emphasize the point that the function name does NOT have to match the name we refer to it by in the config file. The name we refer to the function by in the config file is the string in FunctionType. In this case, we will refer to the functionality we just wrote in the function 'scale_by' with FunctionType.scale_column (which equals 'scale_column')

The corresponding config field for our function in operations would look like this:
```yaml
operations:         # op::scaled_pe
    - output_columns:
        - SCALED_PE
    operation: scale_column
    input_columns:
        - source: bloomberg
        ticker: S5INFT Index
        col_name: PE_RATIO
    arguments: 
        scale: 1.5
        fill_value: 0
    remove: NULL
```
We would call our function with the PE_RATIO column from the S5INFT Index loaded by the model from bloomberg as an input, we will output a new column that can be referred to as "SCALED_PE" and it will be equivalent to the input column with every value scaled by 1.5x and all Na values filled with '0'

Congratualtions! You wrote an operation!

## If You Want to Know How it All Works

Each project stores a list of operation objects which are stored within its self.operations property. 
An operation object has a list of input columns, output columns, columns to be removed, arguments, and a function type. The function type is a string which corresponds to one of the names in the previously discussed FunctionType enum. Here is the constructor for an operation where all of these are set:
```python
def __init__(self, 
                output_columns: List[str],
                operation_type: str, 
                input_columns: List[Dict[str, str]],
                arguments: Dict[str, Any], 
                remove: List[str]):
    if not FunctionType.has_value(operation_type):
        raise ValueError(f'invalid operation {operation_type} provided')
    self.type = FunctionType(operation_type)
    self.arguments: Dict[str, Any] = arguments
    self.remove: List[str] = remove
    self.input_columns: List[NormalizedColumn] = []
    self.output_columns: List[NormalizedColumn] = []

    # keys
    data_source_key = 'source'
    name_key = 'ticker'
    column_name_key = 'col_name'

    for input_col in input_columns:
        self.input_columns.append(NormalizedColumn.from_dict(input_col))

    for output_col in output_columns:
        self.output_columns.append(NormalizedColumn(DataSource.operations, '', output_col))
```

And here is the line in read_config where the operations of each project are initialized 

```python
for raw_operation_config in input_data.get(operations_key, []):
    current_operation = Operation(raw_operation_config[operations_output_columns_key],
                                    raw_operation_config[operation_type_key],
                                    raw_operation_config[operations_input_columns_key],
                                    raw_operation_config.get(operations_arguments_key, {}),
                                    raw_operation_config.get(operations_remove_key, {}))
    new_project.operations.append(current_operation)
```

A normalized column is an obejct we use to store column names so that we can properly trace / modify / pass them around

RunOperations is called in the main.py file 

```python
logger.info(f"Running Operations")
run_operations = RunOperations(project, clean_data, project.operations, args.operations)
```

As you can see, RunOperations runs all of the operations for a project, and then stores the result and saves them to disk

```python
class RunOperations:

    def __init__(self, 
                    global_config: GlobalConfigData, 
                    clean_data: Any,
                    operations: List[Operation], 
                    load_only_fs: bool = False):
        self.basename = f"{normalize_str(global_config.project)}.csv"
        self.data = self._run_operations(clean_data.data, operations, load_only_fs)

    def get_file_path(self) -> str:
        return join(operated_data_folder, self.basename)

    def _run_operations(self, data: pd.DataFrame, operations: List[Operation], load_only_fs: bool) -> pd.DataFrame:
        """
        run list of operations on the data
        """
        file_path = self.get_file_path()
        if load_only_fs:
            if not exists(file_path):
                raise ValueError(f'could not find file {file_path}')
            return load_dataframe_sanitize(file_path)

        for operation in operations:
            # input columns = [normalize_colname(colname) for colname in operation.input_columns]
            # same thing if list comprehensions are your thing
            input_columns = [input_column.normalize_colname() for input_column in operation.input_columns]
            # run the functions
            output_data = function_map[operation.type](data[input_columns], **operation.arguments)

            if not isinstance(output_data, tuple):
                raise ValueError(f'output of operation {operation.type.name} must be a tuple')
            
            for i, current_output_data in enumerate(output_data):
                if len(current_output_data) != len(data):
                    raise ValueError(f'length of output for operation {operation.type.name} != length of dataframe')
                data[operation.output_columns[i].normalize_colname()] = current_output_data

            for remove_column_name in operation.remove:
                del data[remove_column_name]

        logger.success('done with all operations')
        data.to_csv(file_path)

        return data
```

The entire purpose of this object is to populate it's self.data field with the operated data

This line:
```python
for operation in operations:
    # input columns = [normalize_colname(colname) for colname in operation.input_columns]
    # same thing if list comprehensions are your thing
    input_columns = [input_column.normalize_colname() for input_column in operation.input_columns]
    # run the functions
    output_data = function_map[operation.type](data[input_columns], **operation.arguments)
```

Is what calls all of the operations functions from operations_functions.py. The dictionary function_map is a Dict[FunctionType, Callable] which means that it is a dictionary which takes in a FunctionType enum value (string as of now) and a function pointer (or callable). Essentially function_map[FunctionType.scale_column] (args) will be replaced with scale_by(args), the function we wrote earlier. Once the function is called we save the output and continue to the next function. Args are loaded from the config file and saved in the Operation object. 

Direct questions to the head of FactorModel for any questions!