---
id: marginal-risk-of-portfolio-holdings
title: Marginal Risk of Portfolio Holdings
sidebar_label: Marginal Risk of Portfolio Holdings
slug: /marginal-risk-of-portfolio-holdings
---

### Definition:
Each holding in our portfolio contribites to the overall risk of the portfolio. We can quantify that contribution by calculating the marginal contribution to risk. In a more mathematical approach we conceptualize marginal contribtion of risk as the partial derivative of the portfolio's volatility with respect to the waiting of a given asset. This value of marginal contribution to risk can be both negative or positive as we know adding uncorrelated assets to a portfolio reduces the overall risk of the portfolio. Using this metric one can assess whether the purchase of a holding increases or decreses the overall volatility.
A very succint document can be found [here](https://blog.thinknewfound.com/2014/07/risk-attribution-in-a-portfolio/) where it dives into the mathematic derivations and equations for contribution to risk.

### Code:
We begin by calculating the current weight of each holding within our portfolio as a portion of the overall portfolio
```python
  # calculate weights
    tickerValues = [currentPrice * numShares for currentPrice, numShares in zip(currentPrices, shares)]
    totalValue = np.sum(tickerValues)
    weights = [tickerValue / totalValue for tickerValue in tickerValues]
```

Next we calculate the overall standard deviation of the portfolio by iterating through each combination holdings and gathering the variance and correlation between assets.

```python
    # calculate portfolio standard deviation
    portfolioVariance = 0
    for i in range(len(tickers)):
        for j in range(len(tickers)):
            portfolioVariance += weights[i] * weights[j] * np.cov(adjReturns[i], adjReturns[j])[0][1]
    portfolioStdDev = np.sqrt(portfolioVariance)
```

Lastly we calculate the daily contribution to risk of the given ticker and annualize the risk contribution to an annual basis.

```python
    # calculate marginal contribution to risk
    tempSum = 0
    marginalIndex = len(tickers) - 1  # the location of the stock we want to analyze in all the arrays
    for j in range(len(tickers)):
        tempSum += weights[j] * np.cov(adjReturns[marginalIndex], adjReturns[j])[0][1]
    dailyMCTR = (1 / portfolioStdDev) * tempSum

    return dailyMCTR * np.sqrt(252 / 12)
```