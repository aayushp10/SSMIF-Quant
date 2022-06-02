---
id: beta
title: Beta
sidebar_label: Beta
slug: /beta
---

### Investopedia Definition 
Beta is a measure of the volatility—or systematic risk—of a security or portfolio compared to the market as a whole. Beta is used in the capital asset pricing model (CAPM), which describes the relationship between systematic risk and expected return for assets (usually stocks). CAPM is widely used as a method for pricing risky securities and for generating estimates of the expected returns of assets, considering both the risk of those assets and the cost of capital.
[(Full Investopedia Page)](https://www.investopedia.com/terms/b/beta.asp)

### The Code
#### Individual Holdings

```python 
def beta(ticker_data, spy_data) -> int:
    adj_close = ticker_data['Adj Close']
    # daily returns
    daily = adj_close.pct_change().dropna()
    # gets spy data
    spyclose = spy_data['Adj Close']
    spydaily = spyclose.pct_change().dropna()
    # calculating beta

    reg = LinearRegression()
    try:
        reg.fit(spydaily.to_numpy().reshape(-1, 1), daily)
        beta = reg.coef_[0]
    except Exception as e:
        logging.warning(e)
        # print("Mismatch array length")
        return None

    return beta
```

We use the S&P 500 as our benchmark, and use a linear regression model to find the correlation between one of our holdings and the market. "In statistical terms, beta represents the slope of the line through a regression of data points. In finance, each of these data points represents an individual stock's returns against those of the market as a whole." 

#### Different Beta Functions

Our Risk Screen calculates 3 different Beta Values: 
- Market - Measures the selected holding's returns against the S&P 500
- Sector - Measures against only other companies returns in the same sector as the selected holding
- Portfolio - Measures the selected holding against the rest of our portfolio as the benchmark 

While Sector and Portolio Betas don't have a meaningful value for the "Porfolio With / Without" columns, we do calculate how the Aggregate Value of our portfolio's Market Beta is impacted by a given holding. 

```python 
def portfolio_beta(years=3):
    today = date.today()
    spy_data = pdr.get_data_yahoo("^GSPC",str(today.replace(year=today.year - years)))
    weightedReturns = pd.Series(calcDailyWeightedPortfolioReturns(timeRange=years))

    adj_close = pd.Series(weightedReturns)
    # daily returns
    daily = adj_close.dropna()
    # gets spy data
    spyclose = spy_data['Adj Close']
    spydaily = spyclose.pct_change().dropna()
    # calculating beta

    #adjusting for length of lists
    if (len(daily) < len(spydaily)):
        spydaily = spydaily[-(len(daily)):]

    reg = LinearRegression()
    try:
        reg.fit(spydaily.values.reshape(-1,1), daily)
        beta = reg.coef_[0]
    except Exception as e:
        logging.warning(e)
        # print("Mismatch array length")
        return None

    return beta
```

The Code is nearly identical, but rather than using the returns of a single holding, we run the linear regression using the weighted daily returns of our entire portfolio, both with and without the holding included. 




