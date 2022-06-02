---
id: historic-holdings
title: Historic Holdings
sidebar_label: Historic Holdings
slug: /historic-holdings
---

### Developers
- [John Baldi](https://www.linkedin.com/in/john-baldi-4072241a2/)

### Overview

This function generates daily snapshots of our portfolio
holdings.  It parses the SSMIF_HAS transactions csv and updates
the share amount for each transaction.  This data is stored
in the historic_holdings table in the Risk.db database.

:::note
The SSMIF_HAS csv should update automatically as each new transaction
is made, but make sure this is the case so the most updated data is
retrieved.
:::

### How to Run

This data should be updated weekly. It can be updated by
running fillHistoricHoldings() in fillHistoricHoldings.py or can
be updated by following the documentation in updateDatabase.py.