#!/usr/bin/env python
# coding: utf-8

# # Homework 6, Part Two: A dataset about dogs.
# 
# Data from [a FOIL request to New York City](https://www.muckrock.com/foi/new-york-city-17/pet-licensing-data-for-new-york-city-23826/)

# ## Do your importing and your setup

# In[1]:


import pandas as pd


# In[2]:


import matplotlib.pyplot as plt
import numpy as np


# ## Read in the file `NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx` and look at the first five rows

# In[3]:


df = pd.read_excel('NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx', nrows= 30000)
df.head(5)


# ## How many rows do you have in the data? What are the column types?
# 
# If there are more than 30,000 rows in your dataset, go back and only read in the first 30,000.

# In[4]:


df.info()


# ## Describe the dataset in words. What is each row? List two column titles along with what each of those columns means.
# 
# For example: “Each row is an animal in the zoo. `is_reptile` is whether the animal is a reptile or not”

# Each row is a dog license, including data on the dog's description, vaccination, and location
# - 'Owner Zip Code': is the zip code of the dog's owner
# - 'Animal Name': is the dog's name
# - 'Animal Gender': is the dog's gender
# - 'Primary Breed': is the dog's primary breed
# - 'Secondary Breed': is the dog's secondary breed
# - 'Animal Dominant Color': is the dog's primary color
# - 'Animal Secondary Color': is the dog's secondary color
# - 'Animal Third Color': is the dog's other color
# - 'Animal Birth': is the date the dog was born
# - 'Spayed or Neut': describes if the dog was spayed or neutered
# - 'Guard or Trained': describes if the dog's professional status, if any
# - 'Vaccinated': is whether the dog was vaccinated or not
# - 'Application Date': is the applciation date of the license
# - 'License Issued Date': is when the license was issued
# - 'License Expired Date': is when the license will expire

# In[5]:


df.head(2)


# # Your thoughts
# 
# Think of four questions you could ask this dataset. **Don't ask them**, just write them down in the cell below. Feel free to use either Markdown or Python comments.

# - How many professional dogs are there? Does this differ by gender? by breed?
# - How many dogs are spayed or neutered? Does this differ by breed?
# - How long does it take for a license to be issued?
# - What is the most popular dog by ZIP code?

# # Looking at some dogs

# ## What are the most popular (primary) breeds of dogs? Graph the top 10.

# In[6]:


df['Primary Breed'].value_counts().head(10).sort_values().plot(kind = 'barh')


# ## "Unknown" is a terrible breed! Graph the top 10 breeds that are NOT Unknown

# In[7]:


df_known = df[df['Primary Breed'] != 'Unknown']
df_known['Primary Breed'].value_counts().head(10).sort_values().plot(kind = 'barh')


# ## What are the most popular dog names?

# In[8]:


# df_known[~(df_known['Animal Name'].str.contains('unknown', case = False))] <- alternatively, use the ~ method when you have more than 1 thing you want to exclude

df_known = df[(df['Animal Name'] != 'Unknown') & (df['Animal Name'] != "UNKNOWN")]

df_known['Animal Name'].value_counts().head(10).sort_values().plot(kind = 'barh')


# ## Do any dogs have your name? How many dogs are named "Max," and how many are named "Maxwell"?

# In[9]:


#assuming all subsequent questions should exclude unknown information

df_known[(df_known['Animal Name'] == 'Swathi')]
maxwell = df_known[(df_known['Animal Name'] == 'Max') | (df_known['Animal Name'] == 'Maxwell')]
maxwell['Animal Name'].count()


# ## What percentage of dogs are guard dogs?
# 
# Check out the documentation for [value counts](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.value_counts.html).

# In[10]:


((df_known['Guard or Trained'].value_counts(normalize = True)*100)['Yes'])


# ## What are the actual numbers?

# In[11]:


df_known['Guard or Trained'].value_counts()


# ## Wait... if you add that up, is it the same as your number of rows? Where are the other dogs???? How can we find them??????
# 
# Use your `.head()` to think about it, then you'll do some magic with `.value_counts()`

# In[12]:


df_known['Guard or Trained'].count()


# In[14]:


df_known['Guard or Trained'].head()


# In[15]:


df_known['Guard or Trained'].value_counts(dropna = False)


# ## Fill in all of those empty "Guard or Trained" columns with "No"
# 
# Then check your result with another `.value_counts()`

# In[16]:


df_known['Guard or Trained'] = df_known['Guard or Trained'].replace({
    np.nan: 'No'
})


# In[17]:


df_known['Guard or Trained'].value_counts(dropna = False)


# ## What are the top dog breeds for guard dogs? 

# In[18]:


dogs_guard = df_known[(df_known['Guard or Trained'] == 'Yes') & (df_known['Primary Breed'] != 'Unknown')]
dogs_guard['Primary Breed'].value_counts(dropna = False)


# ## Create a new column called "year" that is the dog's year of birth
# 
# The `Animal Birth` column is a datetime, so you can get the year out of it with the code `df['Animal Birth'].apply(lambda birth: birth.year)`.

# In[19]:


df_known["year"] = df_known['Animal Birth'].apply(lambda birth: birth.year)
df_known.head(2)


# ## Calculate a new column called “age” that shows approximately how old the dog is. How old are dogs on average?

# In[20]:


from datetime import date
todays_date = date.today()

df_known['age'] = todays_date.year - df_known.year
df_known.head(2)


# # Joining data together

# ## Which neighborhood does each dog live in?
# 
# You also have a (terrible) list of NYC neighborhoods in `zipcodes-neighborhoods.csv`. Join these two datasets together, so we know what neighborhood each dog lives in. **Be sure to not read it in as `df`, or else you'll overwrite your dogs dataframe.**

# In[ ]:





# In[21]:


df_zip = pd.read_csv('zipcodes-neighborhoods.csv')
df_zip.head()
df_zip.columns


# In[22]:


df_known = df_known.merge(df_zip, left_on='Owner Zip Code', right_on='zip')
df_known.head(2)


# In[23]:


df_known = df_known.drop(columns= ['zip'])


# In[24]:


df_known.head(2)


# In[25]:


df_known.neighborhood.value_counts()


# In[26]:


df_known.borough.value_counts()


# ## What is the most popular dog name in all parts of the Bronx? How about Brooklyn? The Upper East Side?

# In[27]:


# Bronx (borough)
df_known = df_known.rename(columns={
    'Animal Name': 'animal_name',
    "Primary Breed": 'primary_breed',
    "Animal Gender": "gender",
    "Spayed or Neut": "spay",
    "Animal Dominant Color":"color_dom"
})


names_bronx = df_known[df_known.borough == "Bronx"]
names_bronx.animal_name.value_counts().head(1)


# In[28]:


# Brooklyn
names_brooklyn = df_known[df_known.borough == "Brooklyn"]
names_brooklyn.animal_name.value_counts().head(1)


# In[29]:


# Upper East
names_uppereast = df_known[df_known.neighborhood == "Upper East Side"]
names_uppereast.animal_name.value_counts().head(1)


# ## What is the most common dog breed in each of the neighborhoods of NYC?

# In[30]:


df_known = df_known[df_known['primary_breed'] != 'Unknown']

breed_counts = df_known.groupby('neighborhood').primary_breed.value_counts().groupby(level = 0, group_keys = False).nlargest(1).to_frame(name = 'counts')
breed_counts


# ## What breed of dogs are the least likely to be spayed? Male or female?

# In[31]:


df_known.groupby(['spay'])['primary_breed'].value_counts(normalize=True)*100


# In[32]:


df_known.groupby(['spay'])['gender'].value_counts(normalize=True)*100


# ## Make a new column called monochrome that is True for any animal that only has black, white or grey as one of its colors. How many animals are monochrome?

# In[33]:


df_known.columns


# In[34]:


df_known.color_dom.value_counts(dropna=False)


# In[36]:


monochrome_colors = ['black','white','gray','grey']

df_known['monochrome'] = df_known['color_dom'].str.contains('|'.join(monochrome_colors), case = False, na = False)
df_known


# ## How many dogs are in each borough? Plot it in a graph.

# In[37]:


df_known.borough.value_counts().sort_values().plot(kind = 'barh')
plt.title('Number of Dogs in each NYC Borough')


# ## Which borough has the highest number of dogs per-capita?
# 
# You’ll need to merge in `population_boro.csv`

# In[38]:


df_pop = pd.read_csv('boro_population.csv')


# In[39]:


df_pop.head()


# In[40]:


dogs_total = df_known.borough.value_counts().to_frame(name = 'dog_count')
dogs_total


# In[41]:


df_dogcap = dogs_total.merge(df_pop, left_index= True, right_on='borough')
df_dogcap


# In[42]:


df_dogcap['percapita'] = df_dogcap.dog_count/df_dogcap.population
df_dogcap


# ## Make a bar graph of the top 5 breeds in each borough.
# 
# How do you groupby and then only take the top X number? You **really** should ask me, because it's kind of crazy.

# In[43]:


breed_borough5 = pd.DataFrame(df_known.groupby('borough').primary_breed.value_counts().groupby(level = 0, group_keys = False).nlargest(5))

#to change column name use toFrame
breed_borough5 = df_known.groupby('borough').primary_breed.value_counts().groupby(level = 0, group_keys = False).nlargest(5).to_frame(name = 'counts').reset_index()

breed_borough5

#Reference: breed_borough5= df_known.groupby('borough').primary_breed.value_counts().groupby(level = 0, group_keys = False).nlargest(5).to_frame(name = 'counts').reset_index().set_index('borough')  <- will remove 0,1,2... and reset index as the borough


# In[44]:


# Several ways to approach this problem...see https://www.youtube.com/watch?v=O4538i9MQEc for reference
# pd.crosstab(breed_borough5['borough'], breed_borough5['primary_breed'])
# breed_borough5.groupby('borough').primary_breed.value_counts().unstack().plot(kind = 'bar')


# In[45]:


#Each row is a summary - number of dogs of the breed in that part of the city
#Grouped bar charts require each category to be numeric...transformation required - breeds need to be individual columns

breed_borough5.pivot_table(index = 'borough', columns = 'primary_breed') #reshapes the data
# breed_borough5.pivot_table(index = 'borough', columns = 'primary_breed').plot(kind = 'bar') #all the counts in the legends...FIX!


# In[46]:


breed_borough5.pivot_table(index = 'borough', columns = 'primary_breed').plot(kind = 'bar', y = 'counts', figsize=(15, 4))
plt.title('Top 5 Breeds per NYC Borough')
plt.ylabel('Number of Dogs')


# ## What percentage of dogs are not guard dogs?

# In[47]:


df_known['Guard or Trained'].value_counts(normalize = True)*100
(df_known['Guard or Trained'].value_counts(normalize = True)*100)['No']

