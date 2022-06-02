---
id: model-training
title: Model Training
sidebar_label: Model Training
slug: /model-training
---
### Developers
- [Michael DiGregorio](https://www.linkedin.com/in/michael-jonathan-digregorio/)

## How it's Called
- Up first, we have to go over how we get data into all of our models, and how the Factor Model knows which submodels you want to use for training

### How Data is Input

### Model

### SkLearnModel
- All of our ScikitLearn models inherit from the <code>SkLearnModel</code> parent class. This inherits from the abstract base class <code>Model</code>. SkLearnModel defines the functions:
    - <code>saved_model_path</code>
    - <code>save_model</code>
    - <code>load_model</code>
- <code>saved_model_path</code> returns the path of where the model is saved. When we say "saved" we mean the trained model is serialized and saved to disk for future use. This is what is loaded when you skip model training
- <code>save_model</code> serializes the model to <code>pickle</code> and then saves it to the path obtained from <code>saved_model_path</code>
- <code>load_model</code> will load a model from disk (that was saved to <code>pickle</code> format to the path defined by <code>saved_model_path</code>). This is how we retrieve the most recently trained model when you skip training

```python
class BaseModel(SkLearnModel):

    uses_window: bool = False

    def __init__(self, name: str,
                    predictors: List[Dict[str, str]],
                    hyper_parameters: Dict[str, Any],
                    fit_parameters: Dict[str, Any],
                    window_override: Optional[Dict[str, str]] = None):

        super().__init__(name, predictors, hyper_parameters, fit_parameters, window_override)

    def saved_model_path(self) -> str:
        """
        load models from disk
        """
        base_name: str = '_'.join([self.name, f'{self.model_type.name}.pkl'])
        file_path = relative_file_path(join(models_folder, base_name))
        return file_path


    def save_model(self) -> None:
        """
        save models to disk
        """
        file_path = self.saved_model_path()
        with open(file_path, 'wb') as save_model_file:
            pickle.dump(self.model, save_model_file)


    def load_model(self) -> None:
        """
        load model from disk
        """
        file_path = self.saved_model_path()
        with open(file_path, 'rb') as save_model_file:
            self.model = pickle.load(save_model_file)`
```
    
    
### The ARIMA Regression Model
 - The ARIMA Model inherits from the <code>SkLearnModel</code> parent class. An ARIMA Regression is an autoregressive intrgrated moving average model that will predict something based on its own past behaviors and a moving average (in this case a rolling one, however this is customizable with different hyperparameters)

 - The class begins by identifying the model type from the model type enums within the utils folder, setting the current model to <code>None</code>, and the uses_window value . This is all written as follows:

 ```python
 class ArimaRegression(SkLearnModel):
    
    #set the model type as an arima regression
    model_type = ModelType.arima_regression
    model: Optional[ArimaRegression] = None
    uses_window: bool = True
 ```
 
 - We then have the constructor of the class which initializes the parameters, name, predictors, hyper_parameters, fit_parameters, and window_override from the SkLearnModel class. This is done by using super().__init__(). Here is the constructor for the class below. 

 ```python
 def __init__(self, name: str,
                    predictors: List[Dict[str, str]],
                    hyper_parameters: Dict[str, Any],
                    fit_parameters: Dict[str, Any],
                    window_override: Optional[Dict[str, str]] = None):

        self.error = 0.
        super().__init__(name, predictors, hyper_parameters, fit_parameters, window_override)

 ```
### The Random Forest Model

### The Linear Regression Model