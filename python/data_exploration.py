### Dependencie ----------------------------------------------------------------
import pandas as pd # used for working with data sets
import numpy as np # used for working with arrays
import matplotlib.pyplot as plt # used for plotting
import seaborn as sns # used for plotting, see examples at https://seaborn.pydata.org/examples/index.html
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tabulate import tabulate
import re

path_to_data = r"..\data\listings_detail.csv" 

listings = pd.read_csv(path_to_data)


##############################################DATA EXPLORATION#############################################

############ VIEW DATA ##############
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

# Number of elements in the array
listings.size


############ DESCRIBE COLUMN ##############
# Define function to describe each column
def describe_column(column):
    print(f"Column: {column}")
    print(f"Variable type: {listings[column].dtype}")
    print(f"Number of non-null values: {listings[column].notnull().sum()}")
    print(f"Number of unique values: {listings[column].nunique()}")
    
    if listings[column].dtype == 'object':
        print(f"Sample values: {listings[column].sample(5).tolist()}")
        # Generate bar plot for categorical columns
        #plt.figure(figsize=(10, 6))
        #sns.countplot(data=listings, x=column)
        #plt.title(f"Bar plot of {column}")
        #plt.xticks(rotation=45)
        #plt.show()
    else:
        print(f"Minimum value: {listings[column].min()}")
        print(f"Maximum value: {listings[column].max()}")
        print(f"Mean value: {listings[column].mean()}")
        print(f"Standard deviation: {listings[column].std()}")
        # Generate histogram for numeric columns
        #plt.figure(figsize=(10, 6))
        #sns.histplot(data=listings, x=column, bins=30, kde=True)
        #plt.title(f"Histogram of {column}")
        #plt.xlabel(column)
        #plt.ylabel("Frequency")
        #plt.show()
    
    print("\n")

# Describe each column in the dataset
#numeric_columns = listings.select_dtypes(include=['int64', 'float64']).columns
for column in listings.columns:
    describe_column(column)


describe_column('neighbourhood_cleansed')
describe_column('property_type')
describe_column('beds')


########## SUMARIZE COLUMN ##############
# Function to summarize each column
def summarize_column(column):
    data_type = listings[column].dtype
    non_null_count = listings[column].notnull().sum()
    unique_count = listings[column].nunique()
    min_value = listings[column].min() if data_type in ['int64', 'float64'] else None
    max_value = listings[column].max() if data_type in ['int64', 'float64'] else None
    mean_value = listings[column].mean() if data_type in ['int64', 'float64'] else None
    std_dev = listings[column].std() if data_type in ['int64', 'float64'] else None
    
    summary = [column, data_type, non_null_count, unique_count, min_value, max_value, mean_value, std_dev]
    return summary

# List of columns to summarize
columns_to_summarize = listings.columns

# Summarize specified columns
summary_table = []
for column in columns_to_summarize:
    summary_table.append(summarize_column(column))

# Create a DataFrame from the summary
summary_df = pd.DataFrame(summary_table, columns=["Column", "Data Type", "Non-null Count", "Unique Count", "Min Value", "Max Value", "Mean Value", "Standard Deviation"])

# Output the summary to a CSV file
summary_df.to_csv('summary.csv', index=False)


##############################################DATA PREPARATION#############################################

#TODO WITH DATA:
  #Bathroom needs to be ajdusted
  #Price convert to number DONE
  #Reviews convert to numbers

# Handling values
numeric_columns = listings.select_dtypes(include=['int64', 'float64']).columns
categorical_columns = listings.select_dtypes(include=['object']).columns

# Impute missing values for numerical columns with mean
listings[numeric_columns] = listings[numeric_columns].fillna(listings[numeric_columns].mean())

# Feature selection and dropping obsolete columns
exclude_columns = ['scrape_id', 'last_scraped', 'source', 'name', 'description', 'neighbourhood', 
                   'has_availability', 'reviews_per_month', 'amenities']
columns_to_drop = [col for col in exclude_columns if col in listings.columns]
listings = listings.drop(columns=columns_to_drop)

###### Data transformation --->:

# Convert 'price' column to numeric
listings['price'] = listings['price'].replace('[\$,]', '', regex=True).astype(float)



###### Data encoding --->:
# Encoding categorical variables
label_encoders = {}
for column in categorical_columns:
    label_encoders[column] = LabelEncoder()
    listings[column] = label_encoders[column].fit_transform(listings[column])


##############################################DATA MODELING ############################################

# Splitting the data
X = listings.drop(columns=['price'])
y = listings['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Output the preprocessed data
#X_train.to_csv('X_train_regression.csv', index=False)
#y_train.to_csv('y_train_regression.csv', index=False)
#X_test.to_csv('X_test_regression.csv', index=False)
#y_test.to_csv('y_test_regression.csv', index=False)




###########################################################################################################
##############################################CODE FROM TEACHER############################################

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

