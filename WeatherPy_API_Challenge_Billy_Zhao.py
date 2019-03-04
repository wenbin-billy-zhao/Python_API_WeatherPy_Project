#!/usr/bin/env python
# coding: utf-8

# # WeatherPy
# ----
# 
# ### Analysis
# * As expected, the weather becomes significantly warmer as one approaches the equator (0 Deg. Latitude). More interestingly, however, is the fact that the southern hemisphere tends to be warmer this time of year than the northern hemisphere. This may be due to the tilt of the earth.
# * There is no strong relationship between latitude and cloudiness. However, it is interesting to see that a strong band of cities sits at 0, 80, and 100% cloudiness.
# * There is no strong relationship between latitude and wind speed. However, in northern hemispheres there is a flurry of cities with over 20 mph of wind.
# 
# ---
# 
# #### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Dependencies and Setup
import pandas as pd
import numpy as np
import requests
import datetime
import matplotlib.pyplot as plt

from pandas.io.json import json_normalize
import seaborn as sns; sns.set()   # trying a new package called seaborn to generate plots

# Import API key
from config import api_key

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# Output File (CSV)
output_data_file = "output_data/cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)

# Today's time
now = datetime.datetime.now()
todayDate = now.strftime("%m/%d/%Y")


# ## Generate Cities List

# In[2]:


# List for holding lat_lngs and cities
lat_lngs = []
cities = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(low=-90.000, high=90.000, size=1500)
lngs = np.random.uniform(low=-180.000, high=180.000, size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
len(cities)


# ### Perform API Calls
# * Perform a weather check on each city using a series of successive API calls.
# * Include a print log of each city as it'sbeing processed (with the city number and city name).
# 

# In[3]:


# base URL for open weather API
baseURL = "http://api.openweathermap.org/data/2.5/weather?"

# df is the base dataframe with api responses
# I use a json_normalize() function to flatten and normalize json responses into dataframe
df = pd.DataFrame()
x = 1
print('Beginning Data Retrieval')
print('-' * 38)
for city in cities:
    queryUrl = baseURL + 'appid=' + api_key + '&q=' + city + '&units=imperial'
    try:
        response = requests.get(queryUrl).json()
        if response['cod'] == 200:
            print(f"Processing Record data for {x} of Set 1 | {city}")
            df = df.append(json_normalize(response), sort=True)
            x = x+1
        else:
            x = x-1
            pass
    except Exception as e:
        x = x-1
        pass
        


# In[4]:


## check api response data, occasionally, you get humidity reading above 100%
## these are bad data that may skew the plot, so they need to be dropped
df.loc[df['main.humidity'] > 100]


# In[5]:


# show all the column heads of the raw dataframe
list(df)


# In[6]:


# take a look at the columns and raw dataset - there are some odd columns and missing values
df.count()


# In[7]:


# drop humidity > 100% rows, check data integrity
df = df.rename(columns={'main.humidity' : 'humidity'})
df = df[df.humidity <= 100]
df.count()


# ### Convert Raw Data to DataFrame
# * Export the city data into a .csv.
# * Display the DataFrame

# In[8]:


# df1 is modified dataframe with relevent data for final reports
df1 = pd.DataFrame()

df1['City'] = df['name']
df1['Cloudiness'] = df['clouds.all']
df1['Country'] = df['sys.country']
df1['Humidity'] = df['humidity']
df1['Date'] = df['dt']
df1['Latitude'] = df['coord.lat']
df1['Longitude'] = df['coord.lon']
df1['Max Temp'] = df['main.temp_max']
df1['Wind Speed'] = df['wind.speed']

# export results to output csv file
df1.to_csv(output_data_file)

# display dataframe
df1.head()


# In[9]:


# check data integrity - should have same number each columns
df1.count()


# ### Plotting the Data
# * Use proper labeling of the plots using plot titles (including date of analysis) and axes labels.
# * Save the plotted figures as .pngs.

# #### Latitude vs. Temperature Plot

# In[10]:


# plotting Lat vs Temp using 
x = df1['Latitude']
y = df1['Max Temp']
tempPlot = sns.set_style("whitegrid")
tempPlot = sns.scatterplot(x, y, data=df1)
tempPlot.set(xlabel='Latitude', ylabel='Max Tempreture (F)')
plt.title(f'City Latitude vs Max Temperature ({todayDate})')
plt.show()


# #### Latitude vs. Humidity Plot

# In[11]:


x = df1['Latitude']
y = df1['Humidity']
tempPlot = sns.set_style("whitegrid")

plt.title(f'City Latitude ({todayDate})')
tempPlot = sns.scatterplot(x, y, data=df1,)
tempPlot.set(xlabel='Latitude', ylabel='Humidity (%)')
plt.show()


# #### Latitude vs. Cloudiness Plot

# In[12]:


x = df1['Latitude']
y = df1['Cloudiness']
tempPlot = sns.set_style("whitegrid")
tempPlot = sns.scatterplot(x, y, data=df1)
tempPlot.set(xlabel='Latitude', ylabel='Cloudiness (%)')
plt.title(f'City Latitude vs Cloudiness ({todayDate})')
plt.show()


# #### Latitude vs. Wind Speed Plot

# In[13]:


x = df1['Latitude']
y = df1['Wind Speed']
tempPlot = sns.set_style("whitegrid")
tempPlot = sns.scatterplot(x, y, data=df1)
tempPlot.set(xlabel='Latitude', ylabel='Wind Speed (mph)')
plt.title(f'Latitude vs Wind Speed ({todayDate})')
plt.show()

