---
id: setting-up-your-environment
title: Setting Up Your Anaconda Environment
sidebar_label: Setting Up Your Environment
slug: /setting-up-your-environment
---

## What is an Environment and Why Do We Use It?

A virtual environment in Python is a self-contained directory tree that contains a Python installation for a particular version we are using for the project and a number of additional packages that are required for the code to work. To learn more details about managing environments, go to [Python Environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)


## How to Set Up the Factor Model Environment

1. Install Anaconda for your current operating system [here](https://docs.anaconda.com/anaconda/install/). 
    - If you already have Anaconda installed, skip to step 2

1. Open up the terminal and enter the following commands:

### Windows
```bash
git checkout factor_model_development
cd\flaskr\FactorModel
conda env create -f environment_win.yml 
conda activate ssmif_factor_model
```

- When trying to access Anaconda through VSCode or your .cmd terminal, you will need to run the following script if you get a "command not found" error

```bash
 C:\Users\user\Anaconda3\Scripts\activate
 ```
 
### Linux

```bash
git checkout factor_model_development
cd/flaskr/FactorModel
conda env create -f environment.yml 
conda activate ssmif_factor_model
```

### Mac

```bash
git checkout factor_model_development
cd/flaskr/FactorModel
conda env create -f environment_mac.yml 
conda activate ssmif_factor_model
```

:::warning

Note for Mac Users: You are unable to download the blpapi: bloomberg python API through Mac as of Dec 2020.

:::

> If you are having issues with the environments (package not found errors) use pip to install the required packages


## Congratulations!

Your environment is now successfully set up and you are ready to begin exploring the Factor Model
