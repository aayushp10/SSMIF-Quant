---
id: semi-deviation
title: Semi Deviation
sidebar_label: Semi Deviation
slug: /semi-deviation
---

### Investopedia Definition 
Semi-deviation is a method of measuring the below-mean fluctuations in the returns on investment.

Semi-deviation will reveal the worst-case performance to be expected from a risky investment.

Semi-deviation is an alternative measurement to standard deviation or variance. However, unlike those measures, semi-deviation looks only at negative price fluctuations. Thus, semi-deviation is most often used to evaluate the downside risk of an investment.
[(Full Investopedia Page)](https://www.investopedia.com/terms/s/semideviation.asp)

### The Code
#### Individual Holdings

```python
# Returns semi_dev of a given equity
def semi_deviation(ticker_data):
    # Pull and sort returns from ticker data
    ticker_data['Return'] = ticker_data['Adj Close'].pct_change()
    returns = ticker_data['Return'][1:]
    sorted_returns = returns.sort_values(axis=0)
    ###

    # Calculate Semi_dev of returns
    mean = sorted_returns.mean()
    slice = int(len(sorted_returns) / 2)
    lower_returns = (sorted_returns.head(slice))
    cumsum = np.sum((mean - lower_returns) ** 2)
    semi_dev = (1 / len(sorted_returns) * cumsum) ** 0.5
    ###

    return semi_dev
```

The function:
1. Finds the sorted daily returns (as a percentage)
2. Takes only the worst half of our daily returns over the given time period
3. Calculates the sum of [the average return (of the whole window, not just the lowest half) - each of the lowest returns] squared
4. Calculates the semi deviation with the formula 1 / the square root of (the number of days being examined * the cumulative sum) 

#### Portfolio Semi Deviation

```python
# Returns semi_dev of a given equity
def portfolio_semi_deviation(weightedReturns):
    
    adj_close = pd.Series(weightedReturns)
    sorted_returns = adj_close.sort_values(axis=0)

    # Calculate Semi_dev of returns
    mean = sorted_returns.mean()
    slice = int(len(sorted_returns) / 2)
    lower_returns = (sorted_returns.head(slice))
    cumsum = np.sum((mean - lower_returns) ** 2)
    semi_dev = (1 / len(sorted_returns) * cumsum) ** 0.5
    ###

    return semi_dev
```

This function is essentially identical to the one used for individual holdings, but uses the aggregate weighted returns of the entire portfolio. 