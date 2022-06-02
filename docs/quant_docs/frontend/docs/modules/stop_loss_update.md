---
id: stop_loss_update
title: Stop Loss Update
sidebar_label: Stop Loss Update
slug: /stop_loss_update
---

### Developers
- Leo 
- Lasya

### Methodology

This file generates a stop loss report at the end of each week.
The report is created every Friday, after the market closes, and
does not include non-trading days.

### Get Daily Stock Price Function

This function takes in the current date. From there, it returns a
dictionary where all of the keys are the current holdings tickers,
and the value for each key is another dictionary in which the key 
is the date and the value is the stock price for that ticker on 
said day. 

### Check Stop Loss Function

This function takes in the current date, and checks that it is a Friday.
It then proceeds to collect the current holdings and the stop loss data.
Iterate through the current holdings, and check if the stock price for 
that day is less than one of the stop loss values. If so, print which
stop loss and it's value, and the stock price of that day. At the end,
change this dataframe into a HTML readable table to send into the send_email
function.

### Send Email Function

This function takes in the date and a dictionary. The date is used
for the subject of the email. The dictionary is inputted into the 
body of the email, as a table. At the end, calls on the execute_send_email
function to send the email to specified recipients (senior management).

