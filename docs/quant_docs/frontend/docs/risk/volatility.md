---
id: volatility
title: Volatility
sidebar_label: Volatility 
slug: /volatility 
---

### Investopedia Definition 
Volatility is a statistical measure of the dispersion of returns for a given security or market index. In most cases, the higher the volatility, the riskier the security. Volatility is often measured as either the standard deviation or variance between returns from that same security or market index.

In the securities markets, volatility is often associated with big swings in either direction. For example, when the stock market rises and falls more than one percent over a sustained period of time, it is called a "volatile" market. An asset's volatility is a key factor when pricing options contracts.
[(Full Investopedia Page)](https://www.investopedia.com/terms/v/volatility.asp)

### The Code
#### Individual Holdings

```python
# Returns the monthly volatility for a stock upscaled from daily
def Monthly_Volatility(stock_df):
    stock_df = stock_df.dropna()
    returns = stock_df["Adj Close"].pct_change().dropna()
    vol = stats.stdev(returns) * math.sqrt(252 / 12)
    return vol
```

The function:
1. Calculates the standard deviation of our daily returns for a given time period
2. To convert from daily volatility to monthly, multiplies by the square root of 252 / 12

#### Portfolio Volatility

```python
def Monthly_Portfolio_Volatility(weightedReturns):
    vol = stats.stdev(weightedReturns) * math.sqrt(252 / 12)

    return vol
```

This function is essentially identical to the one used for individual holdings, but uses the aggregate weighted returns of the entire portfolio. 

### NOTE

**Our codebase also contains the file CalcMonthlyVolatility.py, but at this time, the function defined in this file isn't referenced anywhere else in our code.**