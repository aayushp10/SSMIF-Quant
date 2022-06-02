Introduction, Michael DiGregorio, Head of Factor Model Development
Will be starting a full time position in Goldman Sachs' Global Markets Engineering Division

Important names: 
    Jeff Nickerson
    Harry Farrell

Information to have on hand for Morningstar:
    Contact: Katherine Gannon
    Base Cost: $4,000 annually
    Including Taxes and Fees: $5,000 annually
    Package: Advanced Morningstar Advisor Workstation
    Update Rate: According to the meeting notes from 2_18 - One month lag (last months end is the last reported value) of daily fund flows for Morningstar Direct

Presentation Script - Factor Model
Slide 22: 
    * The factor model is our asset allocation model
    * Funamental financial inputs to the factor model have not changed since last semester,
    and the current model inputs are listed below
    * Valuation factors are related to sector fundamentals
    * Sentiment factors are used to predict bullish / bearish sentiment among investors
    * Macroeconomic factors used to keep a pulse on how the economy is doing as a whole
    * We are pushing to gain access to Mutual Fund Inflow / Outflow Data for the model so that we can better track how "smart money" is allocating their funds. This would serve as a powerful Sentiment Factor. Currently, this data can be acquired via Morningstar. The data is not available for free anywhere else due to its value

Slide 26:
    * The Factor Model is in the midst of being ported from R to Python 
    * The port is not complete yet, but should be completed by next semester
    * Because of that, we are still using the R model from last semester to generate our current allocations. When the port is complete, it can be configured to match the financials of the old model exactly
    ** This large investment in development time at the expense of fundamental research time was undertaken because it was decided that without the Morningstar Mutual Fund Data, the benefit of further factor research would be outweighed by the benefit of upgrading the model framework **
    ** Going forward, we were quoted at about $5,000 annually for access to the Fund inflow-outflow data. Gaining access would greatly benefit our model **
    ** This investment will pay off in the form of greatly speeding up future model changes and factor research. Previously it would take on the order of weeks to make a meaningful change, with the new framework, that same change could be completed within a day **

Slide 27: 
    * Briefly going over our changes, we can now save the "state" of the model (i.e factor inputs, data transformations, model parameters, general configuration) in a human readable and human writable text file (we call it a configuration file).
    * By changing elements of the configuration file we can manipulate the building blocks of the factor model directly. This allows us to come up with a series of different optimized versions of the Model
    * Below is an example of a data operation. Specifically, we are taking the ratio of the S5INFT Index's PE and PS, and saving it as "PE/PX_TO_SALES_RATIO"

Slide 28: 
    * These changes will allow future analysts to devote significantly less time to development, and significantly more time to fundamental research
    * By generating a "portfolio" of different model configurations (all optimized for different market conditions) the fund can "switch" between models to take full advantage of the current market regime 

    NO
        * One use case would have been in march. Our current model is optimized to generate the best allocations for the market regime as defined pre-covid. When the market went bananas in march, we were unable to take full advantage of the situation. Additionally, our model now has a black swan event in the middle of its input data. By using the new system, we would have been able to switch to a model better able to take advantage of the market circumstance in march. We would have then been able to switch back to our previous configuration (or one optimzied for present market conditions) instantly.
    NO

    * Overall, this will make us a far more agile fund with regards to computer-generated alloations, and better able to take advantage of market shifts

Slide 30:
    * All of this added software complexity did not come cheaply, we saw that there would be a need to better organize our technical documentation, resarch documentation, and new member orientation information. 
    * To address this issue, we created the "Quant Docs" website
    * This website is entirely implemented and is being popualted with tutorials on everything from "how to set up your environment" to "what do we use Total Debt/Total Assets to measure"

Slide 31:
    * Notably, you don't need to know how to code to generate a webpage on our site either. Our system will automatically generate a webpage based off of a "Markdown" text file. Markdown is a simple text styling format. For example, using "##" before a line will make it "Heading 2" just like a word document  
    * Below is an example of a markdown file and the webpage generated from it