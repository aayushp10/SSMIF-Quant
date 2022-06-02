---
id: cvar
title: CVar
sidebar_label: CVar
slug: /cvar
---

### Investopedia Definition 
Conditional Value at Risk (CVaR), also known as the expected shortfall, is a risk assessment measure that quantifies the amount of tail risk an investment portfolio has. CVaR is derived by taking a weighted average of the “extreme” losses in the tail of the distribution of possible returns, beyond the value at risk (VaR) cutoff point. Conditional value at risk is used in portfolio optimization for effective risk management.
[(Full Investopedia Page)](https://www.investopedia.com/terms/c/conditional_value_at_risk.asp)

### The Code
#### Individual Holdings

```python
# Returns the conditional value at risk for a given confidence level.
def Monthly_CVaR(stock_df, confidence_level=0.05):
    returns = stock_df["Adj Close"].pct_change().dropna()
    sortedReturns = sorted(returns)
    cvar = (stats.mean(sortedReturns[0:int(len(sortedReturns) * confidence_level)])) * math.sqrt(252 / 12)

    return cvar
```

The function:
1. Sorts the holdings adjusted returns (as a daily percent change)
2. Takes only the tail of the distribution, meaning if our confidence level is 95% and we have 100 days of returns, we are only looking at the 5 WORST days
3. Takes the average of those returns 
4. To convert daily CVaR to monthly, we multiply by the square root of 252/12 

#### Portfolio CVaR

```python
def Monthly_Portfolio_CVaR(data = None, confidenceLevel=0.05):
    sortedWeightedReturns = sorted(data)
    portfolioCvar = (stats.mean(sortedWeightedReturns[0:int(len(sortedWeightedReturns) * confidenceLevel)])) * math.sqrt(252 / 12)

    return portfolioCvar
```

This function is essentially identical to the one used for individual holdings, but uses the aggregate weighted returns of the entire portfolio. 

### NOTE

**Our codebase also contains the files CalcCvar.py and CalcPortfolioCvar.py, but at this time, neither function defined in those files is referenced anywhere else in our code.**
