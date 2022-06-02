---
id: sdk-overview
title: SSMIF SDK Overview
sidebar_label: SDK Overview
slug: /sdk-overview
---

### Developers

- Joshua Schmidt
- Marcus

### What is an SDK?

SDK stands for software development kit. It's a set of functions and tools that are used by many different projects on the quant team. These utility functions allow for unified database connections, data access, analysis, and computation, avoiding running the same logic many times.

Another term you will hear a lot of is "API". API stands for application program interface, and defines an interface (for lack of a better word) to interact with a given piece of software. API's can come in a number of forms - an imported library, a [REST interface](https://restfulapi.net/), a [GraphQL interface](https://graphql.org/), a [CLI (command line interface)](https://en.wikipedia.org/wiki/Command-line_interface), etc. An API describes an interface, while an SDK contains tools to perform further logic. Typically, an SDK is also an API, but not necessarily the other way around.

### Why make one for the SSMIF?

In the past, we did a lot of the same computation over and over again. We would load historical ticker data from yahoo finance in most of our functions, and calculate metrics like weekly or yearly returns in many different ways. This especially came evident when working on the weekly report module. Additionally, we used sqlite to hold data for Bailey, and we each had different instances of the database installed locally, with no easy way to manage the data in the cloud deployment.

Creating a cloud-deployed sql database would fix these issues, and we decided to switch to PostgreSQL, because it has a feature set that better fits our needs (failover protection, scalability, more allowed datatypes, etc). With the SDK, there is a unified interface and set of tools for managing the database, described below. Utility functions that can be used by multiple teams in quant, for computing data based off of database entries, are also defined in the sdk.

### How does the database connection work?

In order to use any sdk functions / tools that require a database connection, you need to actually connect to the database in your code. There is one function that handles all of this, called `initialize_databases`, located in `ssmif_sdk/models/utils.py`. You would import this by using the following statement: `from ssmif_sdk.models.utils import initialize_databases`, and execute the function in your `__main__` block or, preferrably, in a `main()` function of some sort. The `initialize_databases` function includes arguments for reinitializing data, which essentially clears the database. You DO NOT want to pass in these arguments in production, unless you want to clear the production database (which is rare...).

We're using [peewee](http://docs.peewee-orm.com/en/latest/peewee/quickstart.html) for handling our database connection and modifications. Peewee is an [ORM (object relational mapping library)](https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping). A mapping is a one-to-one representation of data as an object in object-oriented programming (OOP). Instead of writing raw [SQL statements](https://www.codecademy.com/articles/sql-commands), we are creating instances of the class, and calling functions on the class. So in order to add to the `Current_Holdings` table, for example, you would import the `Current_Holdings` model from the `ssmif_sdk/models/current_holdings.py` file, and run `Current_Holdings.create([arguments go here])`. You wouldn't actually want to do this in real life, as there's a utility function for adding and removing current holdings, while keeping track of cash and other transactions (see `ssmif_sdk/utils/execute_transaction.py`), but this is the idea for when you want to write your own utility functions.

### Functionality Overview

The SDK contains functions for connecting to the database and managing data in the database. We already talked about the database connection and models above. In addition, there are tools for helping to build excel files, send emails, get the current and historical stock price, get historical benchmark data, and calculate metrics like nav. Configuration is accomplished using `.env` files (see [this stackoverflow post](https://stackoverflow.com/a/41547163/8623391)), which also enables environment variable configuration.

### Models

A data model, as described above, is a representation of a database object in OOP. These objects can be called members of a database "table", with each row in the table represented by an object. The classes defined in the `ssmif_sdk/models` folder describe the attributes each table has (the columns on the table), and peewee will automatically keep the model in sync with the database (through the `initialize_databases` function). Below is a running list of the models, with a description of what each does:

#### classes

- Base_Model
  - abstract base model, used for storing the database connection for all other models
- Company_Data
  - data for a given company's ticker, such as its name and sector
- Current_Holdings
  - the stocks that we currently own as a fund. includes data like how many shares we purchased and at what price, the original date of purchase, ticker name
- Dividends
  - dividends we received for each of the stocks we own, since the fund first started. this is updated automatically over time
- Historical_Holdings
  - contains historical ticker data, up to the previous trading day. any stocks we own should be included in the table, and if the ticker is not in the table, it is added when creating an instance of the class.
- Sector_Allocations
  - contains the current weights for each of the sectors that we are invested in, and that our benchmark is invested in. this allows us to compare our performance with that of the benchmark. weights for the benchmark update automatically.
- Stop_Loss
  - constains the current stop loss levels for each of our current holdings.
- Team_Members
  - all members of ssmif, currently being used to send emails (like the generated weekly report). may be used for other things in the near future.
- Stock_Transactions
  - ledger of stock buys and sells
- Cash_Deposits
  - ledger of cash deposits
- Cash_Withdrawals
  - ledger of cash withdrawals
  - note - stock transactions, deposits, and withdrawals cannot ever have the exact same datetime index. otherwise the output for the amount of cash on hand, and other metrics, become non-deterministic. In reality, this should never happen, as there are always delays between transactions.

  - TODO - add links to separate docs pages for each class. include an overview of what it does not necessarily exactly how it does it (yet)


### SDK Functions (public interface, not internal stuff)

Current SDK functions include the following:

- `get_daily_weighted_returns` in `ssmif_sdk/utils/daily_weighted_returns.py`
- `get_volatility_annualized` in `ssmif_sdk/utils/daily_weighted_returns.py`
- `get_stock_price` in `ssmif_sdk/utils/stock_price.py`
- `get_benchmark_timeframe` in `ssmif_sdk/utils/stock_price.py`
- `get_benchmark_price` in `ssmif_sdk/utils/stock_price.py`
- `get_nav_timeframe` in `ssmif_sdk/utils/nav.py`
- `get_nav` in `ssmif_sdk/utils/nav.py`

- TODO - add more to the list of functino names, add what they do and how they work, add grouping
- include examples of how to use each one

### Examples

There are many examples of using the utility functions in the `modules/weekly_report/src` directory. You can take a look there to view basic database manipulation and other functions. Examples will be added here soon.

- TODO - an example of using a class and a fucntion or set of them somewhere in ssmif
