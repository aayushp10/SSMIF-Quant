---
id: risk-screen
title: The Risk Screen
sidebar_label: The Risk Screen
slug: /risk-screen
---

### Risk Screen
- #### Why We Use It
    - The Risk Screen is designed to provide risk metrics for financial instruments to the equity analysts. It is designed to screen out any stocks that are deemed to risky for the portfolio. It is a very important tool to evaluate assets for their volatility and other risk metrics.
- #### Inputs
    - ##### Ticker
        - The Ticker is used to represent a specific equity or ETF. That is the ticker for which data will be collected. If a company merges or switches symbols, then data will be lost for that company as the risk screen only tracks a specific ticker symbol.
    - ##### Years
        - The Years input references the amount of time for which the program will go back to recover historical data. It also represents the estimated duration of holding a particular financial instrument. 
    - ##### Sector
        - Sector is used solely for calculating Secotr Beta of an asset.
- #### Data Processing
    - After taking in all the parameters, historical data for that ticker is gathered during that time frame. Then that data is analyzed for specific risk metrics. The output of the risk screen is a table; the rows of the table represent a specific metric for an asset. These metrics all sisplay a different measure of risk of that asset. In conjunction these metrics allow for the analysts to make decsions about whether an asset should be in the portfolio. 
- #### Columns
    - ##### Value
        - For a specific ticker, timeframe, and sector the risk screen will calculate the values for a given set of risk metrics. These values hold little meaning to equity analysts because there is no comparison.
    - ##### Ranking/Percentile
        - The next two columns are the ranking column and the percentile column. The ranking column ranks a specific value against the rest of the portfolio. If the ranking is 1/31 then it is better than all other assets in the portfolio for tha specific metric. If the value is 31/31 then it is worse than all other assets for that specific metric. The percentile column takes the ranking and scales it from 0 to 100. 100th percentile represents the best, while 0th percentile represents the worst.
    - ##### Portfolio With/Portfolio Without
        - The next two columns are the Portfolio With and Portfolio Without columns. As you might be able to guess, these columns show the metric of the entire portfolio with the asset, and the entire portfolio without the asset. This enables the equity analysts to see how the portfolio may change with the addition of a specific asset.
- #### Pass/Fail
    - There is currently a restricition for the portfolio within the IPS that the portfolio can never fall below -15% VaR. If adding a specific financial instrument to the portfolio fails that restriction then the asset fails the risk screen. 