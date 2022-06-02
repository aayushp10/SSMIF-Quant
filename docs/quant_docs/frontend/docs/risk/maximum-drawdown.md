---
id: maximum-drawdown
title: Max Drawdown
sidebar_label: Max Drawdown
slug: /maximum-drawdown
---

### Investopedia Definition 
A maximum drawdown (MDD) is the maximum observed loss from a peak to a trough of a portfolio, before a new peak is attained. Maximum drawdown is an indicator of downside risk over a specified time period.

It can be used both as a stand-alone measure or as an input into other metrics such as "Return over Maximum Drawdown" and the Calmar Ratio. Maximum Drawdown is expressed in percentage terms.
[(Full Investopedia Page)](https://www.investopedia.com/terms/m/maximum-drawdown-mdd.asp)

### The Code
#### Individual Holdings

```python
# Returns the maximum drawdown over a given time period
def max_drawdown(ticker_data):
    window = 252
    Roll_Max = ticker_data['Adj Close'].rolling(window=252, min_periods=1).max()
    Daily_Drawdown = ticker_data['Adj Close'] / Roll_Max - 1.0
    Max_Daily_Drawdown = Daily_Drawdown.rolling(window=252, min_periods=1).min()
    # Daily_Drawdown.plot()
    # Max_Daily_Drawdown.plot()
    # plt.show()
    return Max_Daily_Drawdown[-1]
```

The function:
1. Calculates the Maximum Adjusted close in each year-long rolling window
2. Divides each daily return by the Rolling Maximum - 1
3. Calculates Daily Max Drawdown by again doing a rolling year-long window, but this time taking the Minimum value in each window

#### Portfolio Max Drawdown

```python
# Returns the maximum drawdown over a given time period
def portfolio_max_drawdown(weightedReturns):
    adj_close = pd.Series(weightedReturns)
    window = 252
    Roll_Max = adj_close.rolling(window=252, min_periods=1).max()
    Daily_Drawdown = adj_close / Roll_Max - 1.0
    Max_Daily_Drawdown = Daily_Drawdown.rolling(window=252, min_periods=1).min()
    # Daily_Drawdown.plot()
    # Max_Daily_Drawdown.plot()
    # plt.show()
    return Max_Daily_Drawdown.values.min()
```

This function is essentially identical to the one used for individual holdings, but uses the aggregate weighted returns of the entire portfolio. 