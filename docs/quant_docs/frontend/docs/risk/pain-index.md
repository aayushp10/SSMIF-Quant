---
id: pain-index
title: Pain Index
sidebar_label: Pain Index
slug: /pain-index
---

### Definition 
Numerically, the pain index is the mean value of the drawdowns over the entire analysis period. (See also the definition of the Drawdown statistic.)

### The Code
#### Individual Holdings

```python
def pain_index(ticker_data) -> int:
    adj_close = ticker_data['Adj Close']
    # daily returns
    daily = adj_close.pct_change()
    daily = daily[~np.isnan(daily)]
    # finds average drawdown
    window = 252
    rolling_max = adj_close.rolling(window, min_periods=1).max()
    drawdown = (adj_close - rolling_max) / rolling_max
    # print(drawdown)
    pain_index = sum((abs(drawdown) / (len(drawdown))))
    # print(pain_index)
    return pain_index
```

The function:
1. is well documented with comments :)

#### Portfolio Pain Index

```python
def pain_index(timeRange=3, marginalTicker=None, excluded=None) -> int:
    adj_close = pd.Series(calcDailyWeightedPortfolioReturns(timeRange, marginalTicker, excluded, noPercent=True)).dropna()
    # finds average drawdown
    window = 252
    rolling_max = adj_close.rolling(window, min_periods=1).max()
    drawdown = (adj_close - rolling_max) / rolling_max
    # print(drawdown)
    pain_index = sum((abs(drawdown) / (len(drawdown))))
    # print(pain_index)
    return pain_index
```

This function is essentially identical to the one used for individual holdings, but uses the aggregate weighted returns of the entire portfolio. 