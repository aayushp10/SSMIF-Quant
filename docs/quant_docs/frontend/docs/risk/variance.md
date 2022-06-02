---
id: variance
title: Variance
sidebar_label: Variance
slug: /variance
---

### Investopedia Definition 
The term variance refers to a statistical measurement of the spread between numbers in a data set. More specifically, variance measures how far each number in the set is from the mean and thus from every other number in the set. Variance is often depicted by this symbol: σ2. It is used by both analysts and traders to determine volatility and market security. The square root of the variance is the standard deviation (σ), which helps determine the consistency of an investment's returns over a period of time.
[(Full Investopedia Page)](https://www.investopedia.com/terms/v/variance.asp)

### The Code
#### Individual Holdings

```python
def call_monthly_variance(ticker_data: pd.core.frame.DataFrame) -> int:
    """This function returns the monthly variance of a ticker in the period.
    It calculates on the daily level then scales up by multiplying by 21
    to scale to monthly"""

    ticker_data = ticker_data.dropna()
    
    # Get adjusted close of stock
    adj_close = ticker_data['Adj Close'].pct_change().dropna()

    # returns the monthly variance of the input stock or group of stocks
    daily_variance = np.var(adj_close)
    monthly_variance = daily_variance * (252 / 12)
    return monthly_variance
```

The function:
1. Takes the daily adjusted close values as a percentage of change
2. Uses the built-in Numpy Variance formula
3. To convert from daily to montly Variance, multiplies by the square root of 252 / 12

#### Portfolio Variance

```python
def portfolio_monthly_variance(timeRange=3, marginalTicker=None, excluded=None) -> int:
    """This function returns the monthly variance of a ticker in the period.
    It calculates on the daily level then scales up by multiplying by 21
    to scale to monthly"""

    # Get adjusted close of portfolio
    adj_close = pd.Series(calcDailyWeightedPortfolioReturns(timeRange, marginalTicker, excluded)).dropna()

    # returns the monthly variance of the input stock or group of stocks
    daily_variance = np.var(adj_close)
    monthly_variance = daily_variance * (252 / 12)
    return monthly_variance
```

This function is essentially identical to the one used for individual holdings, but uses the aggregate weighted returns of the entire portfolio. 