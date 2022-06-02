---
id: old-flow
title: R Model Flow
sidebar_label: R Model Flow
slug: /r_model_flow
---

## This is best described with an example

### Assumptions

- Assume the year is 2020, and that the fund has access going back to 2010
- Assume that the investment window is set for 5 years
- Assume that our "error-threshold" is 10% (more on this later)
these predict price 
- Assume the model is composed of a Linear Regression, ARIMA Regression, and Random Forest Regression
so we do a future vol ppredcition the traditional way o.e by lagging our data by as far out as we want to predict  like a month

### Training

- The model is trained on input data from 2010 to 2015
- Translation, you perform traditional training on the three submodels laid out above (linear, arima, forest) over the input window of 2010 - 2015 predicting price
- We then "test" the models based off of "regressive classification accuracy" on the time period from 2015 - 2020
- regressive classification accuracy is a term I just coined which means the following: 
  - a regressive price prediction is considered "correct" if it falls within +/- error_threshold percent of the true value, in this case 10%
linear gets 80% correct 
RF gets 20% correct
ARIMA gets 20% correct

linear = 80/120
RF = 20/120
ARIMA = 20/120

possibly create a floating window based off of the volatility of the benchmark

- volatility idea
- different window size for training
- hrp & black litterman
- no genetic optimziation
- k folds train test split for timeseries
- train for spot prediction? for moving averages, etc

Monte carlo - or multiple predictons - to generate a window or distribution of predcitons. top would be bull case, bottom would be bear case 


generate a spot prediction and use that as the assumption for black litterman
based off of prior knowledge, we think the expected price is x over this number of years, optimize based off of that

check out RNN or other gradient based frameworks for generating factors 

metalabeling

run different market regimes (recession, market boom, wartime) and each has a predetermined slow twitch and fast twitch model weight to balance the monte carlo accordingly. 
based on different monte carlos for each regime type, probability weight each cluster of predictions ranges according to our macro outlook and get final prediction range

^ get 2 outputs, choose the weighting of each output based off of your own predictions of the market

these predict allcoations

we weigh the outputs of these two models based off of our short term vol predction 
65%fast  35% slow
for fast twitch - ver heavily infuence by vol and future vol

slow twicth operates like a black litterman or HRP in the sese that you feed in past-present dfata and fives you an optimzal allcaoiton on that 
we feed in super smooth data so that it pays more attention to large shiftfs in momentum in the market and not weekly or monthly events  


optional k folds...



1, 2,   3, 4,   5, 6,                7, 8,           9, 10,             11, 12,          13, 14,        15, 16

window size 2 weeks

train on jan and feb  - what are we trying to predction 

price       input1      input2
march1        jan1        jan1





useful to have a model matching our old one for calibration

think about sensitivity testing





































