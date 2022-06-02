---
id: example-config
title: Example Config
sidebar_label: Example Config
slug: /example-config
---
### Developers
- [Michael DiGregorio](https://www.linkedin.com/in/michael-jonathan-digregorio/)

```yaml
tech:
  data:
    window:
      start_date: 2020-01-01
      end_date: 2020-11-01
    
    bloomberg:
      S5INFT Index:
        output_basename: NULL # filepath basename (with extension)
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

      S5HLTH Index:
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

      USGG2YR Index:
        cols:
          - PX_LAST
        col_map: []
        
      USGG10YR Index:
        cols:
          - PX_LAST
        col_map: []

      USURTOT Index:
        cols:
          - PX_LAST
        col_map: []

    additional:
      test_data:
        input_path: path.csv
        cols: []
        col_map:
          - old_key: PX_LAST
            new_key: target

    operations:         # op::pe/px_to_sales_ratio
      - output_columns:
          - PE/PX_TO_SALES_RATIO
        operation: take_ratio
        input_columns:
          - source: bloomberg
            ticker: S5INFT Index
            col_name: PE_RATIO
          - source: bloomberg
            ticker: S5INFT Index
            col_name: PX_TO_SALES_RATIO
        
    models:
        - name: LinearRegression
        type: linear_regression
        predictors:
            - source: bloomberg
            ticker: S5INFT Index
            col_name: PX_TO_BOOK_RATIO
            - source: bloomberg
            ticker: S5INFT Index
            col_name: TOT_DEBT_TO_TOT_ASSET
        window_override: 
            start_date: 2020-01-01
            end_date: 2020-05-05
        hyperparams:
            fit_intercept: True
            normalize: False
            n_jobs: -1
        - name: RandomForest
        type: random_forest
        predictors:
            - source: bloomberg
            ticker: S5INDU Index # BB_XLK_PUT_CALL_OPEN_INTEREST_RATIO
            col_name: PX_TO_BOOK_RATIO
        window_override: 
            start_date: 2020-01-01
            end_date: 2020-05-05
        hyperparams:
            n_estimators: 500
            criterion: mse
            max_depth: 5
            min_samples_split: 5
            random_state: 42
            bootstrap: True
        - name: ArimaRegression
        type: arima_regression
        window_override: 
            start_date: 2020-01-01
            end_date: 2020-05-05
        hyperparams:
            order: [5, 1, 0]
        fitparams:
            cov_type: robust

    predict:
        data:
        same_as_train: True
        bloomberg: {} # optional
        additional: {}
        target:
        source: bloomberg
        ticker: S5INDU Index 
        col_name: PX_LAST
        window_size: 10 # number of rows to predict off of at a time
        output_window:
        start_date: 2020-08-01                      # this should be after your data date if you want to really project
        end_date: 2020-11-05

# only one sector is shown above (tech) but if you had several other sectors then you could refer to them by name as we do below
optimize:
    black_litterman:
        predictions:
        - name: 'cons outperform health 5%'
            percentage: 0.05
            weights:
            tech: 0
            cons: 1
            hlth: -1
        - name: 'tech underperform 10%'
            percentage: 0.1
            weights:
            tech: -1
            cons: 0
            hlth: 0
        hyperparams:
        tau_override: []                                 # default estimation is 1 / num_observations
        lower_weight_bound: 0.1
        upper_weight_bound: 0.25
        penalty_constant: -0.1                            # loss = varince + -0.1 * (actual mean returns - target returns)
        market_cap_weights: 
        tech: 0.274
        hlth: 0.141
        cond: 0.116
        tels: 0.112
        fin: 0.099
        indu: 0.084
        cons: 0.07
        util: 0.032
        matr: 0.027
        eng: 0.02

    # hrp:
    #   inputs:
    #     - tech
    #     - hlth
    #     - indu
    #     - matr
    #     - util
```