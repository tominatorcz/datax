### Dependencie ----------------------------------------------------------------
import pandas as pd # used for working with data sets
import numpy as np # used for working with arrays
import matplotlib.pyplot as plt # used for plotting
import seaborn as sns # used for plotting, see examples at https://seaborn.pydata.org/examples/index.html

path_to_data = r"..\data\listings_detail.csv" 

listings = pd.read_csv(path_to_data)

# View data
listings
listings.head(5)
listings.tail(5)

# Get basic data characteristics 
listings.info()
listings.shape
listings.describe()
listings.describe(include='all') 

# List all columns
list(listings.columns)

# Subset data
listings["age"] # columns
listings[0:2] # rows
listings[5:] # rows

listings["age"][0:1] # rows and columns
listings.iloc[[1,2], [1,2]] # integer location
listings.loc[[1,2], ["age", "sex"]] # "name" location
listings.loc[[1,2], listings.columns[3:5]]

# Number of elements in the array
listings.size
listings["age"].size

# Data types
type(listings)
type(listings["age"])

listings.dtypes
listings["age"].dtype
listings.age.dtype

listings = listings.convert_dtypes()
listings.dtypes

# Categorical data
listings["region"].dtype
listings["region"] = listings["region"].astype("category")
listings["region"].dtype

# Create categories from numerical variable
listings["age_cat"] = pd.cut(
  listings["age"],
  [0, 25, 50, 75],
  right=False)

listings["age_cat"].dtype

# Build categories by range
print(list(range(0, 100, 10))) 

# Descriptive statistics
listings.describe()
listings.describe(include='all')

listings["age"].max()
listings["age"].min()
listings["age"].mean()
listings["age"].std()
listings["age"].median()
listings["age"].quantile([0.5])
listings["age"].quantile([0.1, 0.3, 0.6, 0.9])

# Further statistics and values
listings["sex"].count()
listings["sex"].unique()
listings['sex'].value_counts()

# Correlation
listings.corr(numeric_only=True)

# What numbers don't tell
# https://www.autodesk.com/research/publications/same-stats-different-graphs

# Visualise! - package matplotlib, seaborn
# Basic plot - scatter plot

# How many dimensions of data can you show in common scatter plot?

# Statistical plots
# Histogram - shows frequency
listings.hist(['age'])

# Boxplots - shows variability
listings.boxplot(['age'])

# Pair plots
sns.pairplot(listings)

# Correlogram
sns.heatmap(listings.corr(numeric_only=True))

# For more see https://python-graph-gallery.com/

# Stay AWAY from pie plots unless you have something to hide
# https://www.data-to-viz.com/caveat/pie.html

# Data by groups
listings.groupby(by=["region"], dropna=False).mean(numeric_only=True)
listings.groupby(by=["region"], dropna=False).min()

# Filter data
data_new = listings[(listings.region == "northwest") & 
(listings.sex == "male")]

# Creating the Second Dataframe using dictionary 
data_new = pd.DataFrame({"age":[30, 50, 60, 19], 
                        "sex":["male", "female", "male", "female"],
                        "bmi":[18, 26, 37, 27.9],
                        "children":[1, 20, 2, 0],
                        "smoker":[np.nan, np.nan, np.nan, "yes"],
                        "region":["southnorth", "southeast", "northwest", "southwest"],
                        "charges":[100, 16000, 27000, 16884.924],
                        "age_cat":[np.nan, np.nan, np.nan, "[0.0,25.0)"]}) 

# Create new incorrect data
data_incorrect = pd.concat([listings, data_new], ignore_index=True)

# What has changed?
data_incorrect["age"].mean()
data_incorrect["age"].median()
# What has changed?
data_incorrect["region"].count()
data_incorrect["region"].unique()

# Is null, na value
data_incorrect.isnull()
data_incorrect[data_incorrect.isna().any(axis=1)]

# If the value is northsouth, set it to southeast:
for x in data_incorrect.index:
  if data_incorrect.loc[x, "region"] == "northsouth":
    data_incorrect.loc[x, "region"] = "southeast"

# Delete rows where "region" is northsouth:
for x in data_incorrect.index:
  if data_incorrect.loc[x, "region"] == "northsouth":
    data_incorrect.drop(x, inplace = True)

# Remove rows with a NULL value in the "Date" column:
data_incorrect.dropna(subset=["smoker"], inplace = True)

# Removing Duplicates
data_incorrect.duplicated()
data_incorrect.drop_duplicates(inplace = True)


### Data about Australian weather ----------------------------------------------
# source: https://rdrr.io/github/grayskripko/rattle/man/weather.html
# path: weather_data.csv (in files on MS Teams)
# Weather observations from a number of locations around Australia

path_to_data = "c:/Users/filip/Documents/Resources/Výuka/DataX/2022_2023_ZS/weather_data.csv" 

data_weather = pd.read_csv(path_to_data, encoding = 'UTF-8')

# Hint
# Convert to date
# df['Date'] = pd.to_datetime(df['Date']) 

