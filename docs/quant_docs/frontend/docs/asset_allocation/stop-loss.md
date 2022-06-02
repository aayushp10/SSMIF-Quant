---
id: stop-loss
title: Stop Loss
sidebar_label: Stop Loss
slug: /stop-loss
---

### Developers
- [Eden Luvishis](https://www.linkedin.com/in/eden-l-b826b6132/)
- Joshua

### Methodology

The Sigmoid Stop Loss uses a volatility based risk ratio as its standard measurement of 
risk. The risk ratio is computed by dividing the volatility of the asset by the volatility
of the benchmark index. The stop loss levels are then based on running the risk ratio through 
the predefined sigmoid function. 

### Stop Loss Function
The stop loss function takes the following arguments: 
- tickers: a list of tickers
- benchmark: a string of the ticker of the benchmark index
- risk_function: used to compute risk (default is standard deviation)
- stop_function: used to compute first stop value as a function of risk ratio

### Visualization
Click here to visualize the [sigmoid function](https://www.desmos.com/calculator/60vlsja6sj).

### Stop Loss Levels
- 1st stop value is the direct output of the the sigmoid function. 
- 2nd stop value is 1.25 times the first. 
- 3rd stop value is 1.5 times the first.

### Updating Stop Loss Levels

The check_trailing_stops function ensures that the stop values only get updated if the stock
goes up in price and has higher stop values. Otherwise, the stop levels remain the same as when they were last calculated
and show what date they were last updated. 

### Updating Stop Loss Table
Uncomment and run the following lines in the _main_ function calcSignmoidStops.py

:::note

The table should be updated every semester.
:::

```python
 conn = sq.connect(dbfile)
 final_stop_price_date_df.to_sql("stop_loss", conn, index=True, index_label="Ticker", if_exists="replace")
```