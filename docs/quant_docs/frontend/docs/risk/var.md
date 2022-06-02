---
id: var
title: Var
sidebar_label: Var
slug: /var
---

### Investopedia Definition 
The most popular and traditional measure of risk is volatility. The main problem with volatility, however, is that it does not care about the direction of an investment's movement: stock can be volatile because it suddenly jumps higher. Of course, investors aren't distressed by gains.

For investors, the risk is about the odds of losing money, and VAR is based on that common-sense fact. By assuming investors care about the odds of a really big loss, VAR answers the question, "What is my worst-case scenario?" or "How much could I lose in a really bad month?"

Now let's get specific. A VAR statistic has three components: a time period, a confidence level and a loss amount (or loss percentage. Keep these three parts in mind as we give some examples of variations of the question that VAR answers:

- What is the most I can—with a 95% or 99% level of confidence—expect to lose in dollars over the next month?
- What is the maximum percentage I can—with 95% or 99% confidence—expect to lose over the next year?

You can see how the "VAR question" has three elements: a relatively high level of confidence (typically either 95% or 99%), a time period (a day, a month or a year) and an estimate of investment loss (expressed either in dollar or percentage terms).
[(Full Investopedia Page)](https://www.investopedia.com/articles/04/092904.asp)

### The Code
#### Individual Holdings

```python
# returns the value at risk based on a stock's historical prices
def Monthly_VaR(stock_df, confidence_level=0.05):
    returns = stock_df["Adj Close"].pct_change().dropna()
    sortedReturns = sorted(returns)
    var = sortedReturns[int(len(sortedReturns) * confidence_level)] * math.sqrt(252 / 12)

    return var
```

The function:
1. Sorts the holdings adjusted returns (as a daily percent change)
2. Chops off the tail of the distribution, meaning if our confidence level is 95% and we have 100 days of returns, we are NOT interested in the worst 5 days
3. Takes the average of those returns 
4. To convert daily CVaR to monthly, we multiply by the square root of 252/12 

#### Portfolio VaR

```python
def Monthly_Portfolio_VaR(data = None, confidenceLevel=0.05):
    sortedWeightedReturns = sorted(data)
    portfolioVar = (sortedWeightedReturns[int(len(sortedWeightedReturns) * confidenceLevel)]) * math.sqrt(252 / 12)

    return portfolioVar
```

This function is essentially identical to the one used for individual holdings, but uses the aggregate weighted returns of the entire portfolio. 

### NOTE

**Our codebase also contains the files CalcVar.py and CalcPortfolioVar.py, but at this time, neither function defined in those files is referenced anywhere else in our code.**