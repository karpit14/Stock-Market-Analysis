#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___

# # Finance Data Project 
# 
# In this data project we will focus on exploratory data analysis of stock prices. Keep in mind, this project is just meant to practice your visualization and pandas skills, it is not meant to be a robust financial analysis or be taken as financial advice.
# ____
# ** NOTE: This project is extremely challenging because it will introduce a lot of new concepts and have you looking things up on your own (we'll point you in the right direction) to try to solve the tasks issued. Feel free to just go through the solutions lecture notebook and video as a "walkthrough" project if you don't want to have to look things up yourself. You'll still learn a lot that way! **
# ____
# We'll focus on bank stocks and see how they progressed throughout the [financial crisis](https://en.wikipedia.org/wiki/Financial_crisis_of_2007%E2%80%9308) all the way to early 2016.

# ## Get the Data
# 
# In this section we will learn how to use pandas to directly read data from Google finance using pandas!
# 
# First we need to start with the proper imports, which we've already laid out for you here.
# 
# *Note: [You'll need to install pandas-datareader for this to work!](https://github.com/pydata/pandas-datareader) Pandas datareader allows you to [read stock information directly from the internet](http://pandas.pydata.org/pandas-docs/stable/remote_data.html) Use these links for install guidance (**pip install pandas-datareader**), or just follow along with the video lecture.*
# 
# ### The Imports
# 
# Already filled out for you.

# In[1]:


from pandas_datareader import data, wb
import pandas as pd
import numpy as np
import datetime
get_ipython().run_line_magic('matplotlib', 'inline')


# ## Data
# 
# We need to get data using pandas datareader. We will get stock information for the following banks:
# *  Bank of America
# * CitiGroup
# * Goldman Sachs
# * JPMorgan Chase
# * Morgan Stanley
# * Wells Fargo
# 
# ** Figure out how to get the stock data from Jan 1st 2006 to Jan 1st 2016 for each of these banks. Set each bank to be a separate dataframe, with the variable name for that bank being its ticker symbol. This will involve a few steps:**
# 1. Use datetime to set start and end datetime objects.
# 2. Figure out the ticker symbol for each bank.
# 2. Figure out how to use datareader to grab info on the stock.
# 
# ** Use [this documentation page](https://pandas-datareader.readthedocs.io/en/latest/remote_data.html) for hints and instructions (it should just be a matter of replacing certain values. Use google finance as a source, for example:**
#     
#     # Bank of America
#     BAC = data.DataReader("BAC", 'google', start, end)
# 
# ### WARNING: MAKE SURE TO CHECK THE LINK ABOVE FOR THE LATEST WORKING API. "google" MAY NOT ALWAYS WORK. 
# ------------
# ### We also provide pickle file in the article lecture right before the video lectures.

# In[2]:


start=datetime.datetime(2006,1,1)
end=datetime.datetime(2016,1,1)


# In[3]:


import pandas_datareader.data as web

BAC = web.DataReader('BAC', 'yahoo', start, end)
C = web.DataReader('C', 'yahoo', start, end)
GS = web.DataReader('GS', 'yahoo', start, end)
JPM = web.DataReader('JPM', 'yahoo', start, end)
MS = web.DataReader('MS', 'yahoo', start, end)
WFC = web.DataReader('WFC', 'yahoo', start, end)


# In[ ]:





# ** Create a list of the ticker symbols (as strings) in alphabetical order. Call this list: tickers**

# In[4]:


tickers=['BAC','C','GS','JPM','MS','WFC']
tickers


# ** Use pd.concat to concatenate the bank dataframes together to a single data frame called bank_stocks. Set the keys argument equal to the tickers list. Also pay attention to what axis you concatenate on.**

# In[5]:


bank_stocks=pd.concat([BAC,C,GS,JPM,MS,WFC],axis=1,keys=tickers)


# ** Set the column name levels (this is filled out for you):**

# In[6]:


bank_stocks.columns.names = ['Bank Ticker','Stock Info']
bank_stocks.head()


# # EDA
# 
# Let's explore the data a bit! Before continuing, I encourage you to check out the documentation on [Multi-Level Indexing](http://pandas.pydata.org/pandas-docs/stable/advanced.html) and [Using .xs](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.xs.html).
# Reference the solutions if you can not figure out how to use .xs(), since that will be a major part of this project.
# 
# ** What is the max Close price for each bank's stock throughout the time period?**

# In[7]:


bank_stocks.xs('Close',axis=1,level=1).max()


# ** Create a new empty DataFrame called returns. This dataframe will contain the returns for each bank's stock. returns are typically defined by:**
# 
# $$r_t = \frac{p_t - p_{t-1}}{p_{t-1}} = \frac{p_t}{p_{t-1}} - 1$$

# In[8]:


returns=pd.DataFrame()


# ** We can use pandas pct_change() method on the Close column to create a column representing this return value. Create a for loop that goes and for each Bank Stock Ticker creates this returns column and set's it as a column in the returns DataFrame.**

# In[9]:


for tick in tickers:
    returns[tick+' Return']=bank_stocks[tick]['Close'].pct_change()
returns.head()


# ** Create a pairplot using seaborn of the returns dataframe. What stock stands out to you? Can you figure out why?**

# In[10]:


import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
sns.pairplot(data=returns,aspect=1)
#plt.tight_layout()


# ** Using this returns DataFrame, figure out on what dates each bank stock had the best and worst single day returns. You should notice that 4 of the banks share the same day for the worst drop, did anything significant happen that day?**

# In[11]:


returns.idxmin()
#worst
#Wall Street provided an unwelcome reminder of the financial challenge facing Barack Obama as it marked the new president's inauguration with a stock market plunge led down by a renewed crisis of confidence in US banks.


# ** You should have noticed that Citigroup's largest drop and biggest gain were very close to one another, did anythign significant happen in that time frame? **

# In[12]:


returns.idxmax()
#best


# ** Take a look at the standard deviation of the returns, which stock would you classify as the riskiest over the entire time period? Which would you classify as the riskiest for the year 2015?**

# In[13]:


returns.std()
#citigroup is riskiest


# In[ ]:





# In[14]:


returns.loc['2015-1-1':'2015-12-31'].std()
#MS is the riskiest followed by BAC


# In[ ]:





# ** Create a distplot using seaborn of the 2015 returns for Morgan Stanley **

# In[15]:


sns.distplot(returns.loc['2015-1-1':'2015-12-31']['MS Return'],color='green',bins=100)


# In[ ]:





# ** Create a distplot using seaborn of the 2008 returns for CitiGroup **

# In[16]:


sns.distplot(returns.loc['2008-1-1':'2008-12-31']['C Return'],color='red',bins=100)


# In[ ]:





# ____
# # More Visualization
# 
# A lot of this project will focus on visualizations. Feel free to use any of your preferred visualization libraries to try to recreate the described plots below, seaborn, matplotlib, plotly and cufflinks, or just pandas.
# 
# ### Imports

# In[17]:


import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
get_ipython().run_line_magic('matplotlib', 'inline')

# Optional Plotly Method Imports
import plotly
import cufflinks as cf
cf.go_offline()


# ** Create a line plot showing Close price for each bank for the entire index of time. (Hint: Try using a for loop, or use [.xs](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.xs.html) to get a cross section of the data.)**

# In[18]:


bank_stocks.xs('Close',axis=1,level=1).iplot()


# In[ ]:





# In[ ]:





# ## Moving Averages
# 
# Let's analyze the moving averages for these stocks in the year 2008. 
# 
# ** Plot the rolling 30 day average against the Close Price for Bank Of America's stock for the year 2008**

# In[19]:


bank_stocks.loc['2008-1-1':'2008-12-31'].xs(('BAC','Close'),axis=1).plot(figsize=(12,5),color='green')
bank_stocks.loc['2008-1-1':'2008-12-31'].xs(('BAC','Close'),axis=1).rolling(window=30).mean().plot(color='blue')
plt.legend(['BAC Close','30 Day Avg'])


# In[ ]:





# ** Create a heatmap of the correlation between the stocks Close Price.**

# In[20]:


sns.heatmap(bank_stocks.xs('Close',axis=1,level=1).corr(),annot=True)


# In[ ]:





# ** Optional: Use seaborn's clustermap to cluster the correlations together:**

# In[21]:


sns.clustermap(bank_stocks.xs('Close',axis=1,level=1).corr(),annot=True)


# In[ ]:





# In[ ]:





# # Part 2 (Optional)
# 
# In this second part of the project we will rely on the cufflinks library to create some Technical Analysis plots. This part of the project is experimental due to its heavy reliance on the cuffinks project, so feel free to skip it if any functionality is broken in the future.

# ** Use .iplot(kind='candle) to create a candle plot of Bank of America's stock from Jan 1st 2015 to Jan 1st 2016.**

# In[22]:


bank_stocks.loc['2015-1-1':'2016-1-1'].xs('BAC',axis=1).iplot(kind='candle')


# ** Use .ta_plot(study='sma') to create a Simple Moving Averages plot of Morgan Stanley for the year 2015.**

# In[23]:


bank_stocks.loc['2015-1-1':'2015-12-31'].xs('MS',axis=1).ta_plot(study='sma')


# **Use .ta_plot(study='boll') to create a Bollinger Band Plot for Bank of America for the year 2015.**

# In[ ]:





# # Great Job!
# 
# Definitely a lot of more specific finance topics here, so don't worry if you didn't understand them all! The only thing you should be concerned with understanding are the basic pandas and visualization oeprations.
