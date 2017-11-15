
# coding: utf-8

# ## ---
# 
# _You are currently looking at **version 1.5** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# # Assignment 3 - More Pandas
# This assignment requires more individual learning then the last one did - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

# ### Question 1 (20%)
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
# 
# Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 
# 
# e.g. 
# 
# `'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
# 
# `'Switzerland17'` should be `'Switzerland'`.
# 
# <br>
# 
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# <br>
# 
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
# 
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# 
# *This function should return a DataFrame with 20 columns and 15 entries.*

# In[1]:

def answer_one():
    
    import numpy as np
    import pandas as pd
    energy=pd.read_excel('Energy Indicators.xls', na_values='...')
    energy=energy[16:243]
    energy.drop(energy.columns[[0,1]], axis=1, inplace=True)
    energy.columns=['Country', 'Energy Supply', 'Energy Supply per Capita','% Renewable']
    energy['Energy Supply']*=1000000
    
    for row in energy.index:
        for j in energy.loc[row, 'Country']:
            if j.isalpha()==False and j!=' ' and j!=',' and j!='-': 
                z=energy.loc[row, 'Country']
                x=z.index(j)
                y=z[:x]
                if y[-1]==' ':
                    y=y[:-1]
                energy.loc[row, 'Country']=y
                break

    energy.loc[energy['Country']=='Republic of Korea', 'Country']='South Korea'
    energy.loc[energy['Country']=='United States of America', 'Country']='United States'
    energy.loc[energy['Country']=='United Kingdom of Great Britain and Northern Ireland', 'Country']='United Kingdom'
    energy.loc[energy['Country']=='China, Hong Kong Special Administrative Region', 'Country']='Hong Kong'


    GDP=pd.read_csv('world_bank.csv',header=4)
    GDP.loc[GDP['Country Name']=='Korea, Rep.','Country Name']='South Korea'
    GDP.loc[GDP['Country Name']=='Iran, Islamic Rep.', 'Country Name']='Iran'
    GDP.loc[GDP['Country Name']=='Hong Kong SAR, China', 'Country Name']='Hong Kong'

    GDP=GDP.iloc[:,[0, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]]
    GDP.columns=['Country', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']

    ScimEn=pd.read_excel('scimagojr-3.xlsx')

    x= pd.merge(pd.merge(ScimEn, energy, on='Country'),GDP, on='Country').set_index('Country')
    z=x.iloc[:15]
    return z
answer_one()


# ### Question 2 (6.6%)
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This function should return a single number.*

# In[2]:

get_ipython().run_cell_magic('HTML', '', '<svg width="800" height="300">\n  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />\n  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />\n  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />\n  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>\n  <text  x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>\n</svg>')


# In[3]:

def answer_two():
    import pandas as pd
    energy=pd.read_excel('Energy Indicators.xls', na_values='...')
    energy=energy[16:243]
    energy.drop(energy.columns[[0,1]], axis=1, inplace=True)
    energy.columns=['Country', 'Energy Supply', 'Energy Supply per Capita','% Renewable']

    GDP=pd.read_csv('world_bank.csv',header=4)
    GDP=GDP.iloc[:,[0, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]]
    GDP.columns=['Country', '2006', '2007', '2008', '2009', '2010', '2011', '2012','2013', '2014', '2015']

    ScimEn=pd.read_excel('scimagojr-3.xlsx')

    x=pd.merge(pd.merge(ScimEn, energy, on='Country', how='outer'),GDP, on='Country', how='outer').set_index('Country')
    y=pd.merge(pd.merge(ScimEn, energy, on='Country', how='inner'),GDP, on='Country', how='inner').set_index('Country')
    z=len(x)-len(y)
  
    return z
answer_two()


# <br>
# 
# ## Answer the following questions in the context of only the top 15 countries by Scimagojr Rank (aka the DataFrame returned by `answer_one()`)

# ### Question 3 (6.6%)
# What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
# 
# *This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*

# In[4]:

def answer_three():
    Top15 = answer_one()
    aa=Top15.loc[:, '2006':'2015']
    avgGDP=aa.mean(axis=1).sort_values(ascending=False)
    return avgGDP
answer_three()


# ### Question 4 (6.6%)
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# 
# *This function should return a single number.*

# In[5]:

def answer_four():
    Top15 = answer_one()
    c6=answer_three().index[5]
    res=abs((Top15.loc[c6, '2006'])-(Top15.loc[c6, '2015']))
    return res
answer_four()


# ### Question 5 (6.6%)
# What is the mean `Energy Supply per Capita`?
# 
# *This function should return a single number.*

# In[6]:

def answer_five():
    import numpy as np
    Top15 = answer_one()
    return np.mean(Top15['Energy Supply per Capita'])
answer_five()


# ### Question 6 (6.6%)
# What country has the maximum % Renewable and what is the percentage?
# 
# *This function should return a tuple with the name of the country and the percentage.*

# In[7]:

def answer_six():
    import numpy as np
    Top15 = answer_one()
    a=Top15['% Renewable'].where(Top15['% Renewable']==np.max(Top15['% Renewable'])).dropna()
    return (a.index[0], a[0])
answer_six()


# ### Question 7 (6.6%)
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This function should return a tuple with the name of the country and the ratio.*

# In[8]:

def answer_seven():
    import numpy as np
    Top15 = answer_one()
    Top15['ratio']=Top15['Self-citations']/Top15['Citations']
    a=Top15['ratio'].where(Top15['ratio']==np.max(Top15['ratio'])).dropna()
    return (a.index[0], a[0])
answer_seven()


# ### Question 8 (6.6%)
# 
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
# What is the third most populous country according to this estimate?
# 
# *This function should return a single string value.*

# In[9]:

def answer_eight():
    Top15 = answer_one()
    Top15['Pop']=Top15['Energy Supply']/Top15['Energy Supply per Capita']
    a=Top15['Pop'].sort_values(ascending=False)
    return a.index[2]
answer_eight()


