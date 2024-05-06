### Dependencie ----------------------------------------------------------------
import pandas as pd # used for working with data sets
import numpy as np # used for working with arrays
import matplotlib.pyplot as plt # used for plotting
import seaborn as sns # used for plotting, see examples at https://seaborn.pydata.org/examples/index.html
import glob

# Read the combined CSV file into a DataFrame
listings = pd.read_csv(r"..\data\listings_detail_9-23.csv")


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
"""Tomi funkce:
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
"""
def describe_column(column):
    print(f"Column: {column}")
    print(f"Variable type: {listings[column].dtype}")
    print(f"Number of non-null values: {listings[column].notnull().sum()}")
    print(f"Number of missing values: {listings[column].isnull().sum()}")
    print(f"Number of unique values: {listings[column].nunique()}")
    
    if listings[column].dtype == 'object':
        print(f"Type of values: Categorical")
        print(f"Sample values: {listings[column].sample(5).tolist()}")
    else:
        print(f"Type of values: Numerical")
        print(f"Minimum value: {listings[column].min()}")
        print(f"Maximum value: {listings[column].max()}")
        print(f"Mean value: {listings[column].mean()}")
        print(f"Standard deviation: {listings[column].std()}")
        
        # Detect and handle outliers (you might need to customize this part based on your definition of outliers)
        Q1 = listings[column].quantile(0.05)
        Q3 = listings[column].quantile(0.95)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = (listings[column] < lower_bound) | (listings[column] > upper_bound)
        print(f"Number of outliers: {outliers.sum()}")


# Describe each column in the dataset
#numeric_columns = listings.select_dtypes(include=['int64', 'float64']).columns
for column in listings.columns:
    describe_column(column)

describe_column('neighbourhood_cleansed')
describe_column('property_type')
describe_column('last_scraped')


########## SUMARIZE COLUMN ##############
# Function to summarize each column
"""Tomi code
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
"""
def summarize_column(column):
    data_type = listings[column].dtype
    non_null_count = listings[column].notnull().sum()
    missing_count = listings[column].isnull().sum()  # Count of missing values
    unique_count = listings[column].nunique()
    
    if data_type in ['int64', 'float64']:
        min_value = listings[column].min()
        max_value = listings[column].max()
        mean_value = listings[column].mean()
        std_dev = listings[column].std()
        
        # Outlier detection
        Q1 = listings[column].quantile(0.05)
        Q3 = listings[column].quantile(0.95)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = (listings[column] < lower_bound) | (listings[column] > upper_bound)
        outlier_count = outliers.sum()
        
        summary = [column, data_type, non_null_count, missing_count, unique_count, min_value, max_value, mean_value, std_dev, outlier_count]
    else:
        min_value = None
        max_value = None
        mean_value = None
        std_dev = None
        outlier_count = None
        
        summary = [column, data_type, non_null_count, missing_count, unique_count, min_value, max_value, mean_value, std_dev]
    
    return summary


# List of columns to summarize
columns_to_summarize = listings.columns

# Summarize specified columns
summary_table = []
for column in columns_to_summarize:
    summary_table.append(summarize_column(column))

# Create a DataFrame from the summary
summary_df = pd.DataFrame(summary_table, columns=["Column", "Data Type", "Non-null Count", "Missing Count", "Unique Count", "Min Value", "Max Value", "Mean Value", "Standard Deviation", "Outlier Count"])

# Output the summary to a CSV file
summary_df.to_csv('summary.csv', index=False)


