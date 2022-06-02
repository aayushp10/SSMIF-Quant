# Factor Model

> factor model code

Installation:
- conda env create --file environment.yml (if on windows: environment_win.yml)
- if you are going to be running the blpapi: python -m pip install --index-url=https://bloomberg.bintray.com/pip/simple blpapi
- To export an environment: conda env export --no-builds | grep -v "^prefix: " > environment.yml
- To remove an environment: conda env remove --name ENV_NAME (make sure you don't have that environment activated)
- To activate an environment: conda activate ENV_NAME
- To deactivate an environment: conda deactivate ENV_NAME

THE PARADIGM: Factor Model Style Guide

- Variables which are only used in a single file and should not be user-exopsed should be defined within that file 
- Variables used within multiple files or which should be user-exposed should be defined within the constants.py file
- Functions which are only used within one file should be defined within that file
- Functions used within multiple files and logically do not belong in either place should be defined in a utils or shared file
- If a file for a particular task gets too big then it becomes a folder, with an internal file for each major component
- pylint should be run on all code
- Errors and Exceptions should be explicitely raised in the event of a non-conforming parameter or output. Do not let errors go silently
- Avoid global variables
- Use default iterators on objects which support them
- Avoid deprecated features wherever possible
- Function docstrings are required
- Class docstrings are required
- Module docstrings are required
- We use trailing commas
- No trailing whitepace
- We use space between mathematical operations
- We use shebang lines on all files which may be executed directly
- Use format strings, do not do this: print('hello there' + name + 'how are you')
- Pick a type of string (", ') and stick with it
- Explicitely close files and sockets when not using them - use the 'with' statement
- TODO statements should have mirrors in the GitHub issues and should be formated as # TODO(name): What you have to do
- Imports of modules should be on separate lines
- Imports should be sorted lexicographically, ignoring case, according to each modules full path. May place a blank line between import sections
- Generally one statement per linel
- Variable names should eschew abbreviateion wherever possible and follow the snake_case_convention
- Do not use dashes (-) in variable, module, or folder names. Use underscore (_)
- CapWords for class names
- Code should always check if _ _name_ _ == "_ _main_ _"
- Code should always contain a main function if it contains execution logic
- Prefer small and focused functions
- Use explicit Optional[Text] declration for function arguments rather than an implicit one 
- Use typing wherever possible and import the classes themselves from the typing module
- Avoid circular dependencies
- BE CONSISTENT


MODEL LAYOUT
- When we train our regressive models we will lag each of the columns a different amount depending on historical correlation with the price of the asset in question
- We will regularize the the columns according to a uniform metric so that we capture the time-adjusted impact over time of each factor going into the factor model
- We will use our regression models to generate a price prediction for n months out
- The returns of that predicted price over time will become our "expected returns"
- Once we have generated our expected returns vector we can optimize our portfolio using a non-black-boxed approach ex: Hierarchal Risk Parity, Black Litterman, Mean-Variance Optimization, ...