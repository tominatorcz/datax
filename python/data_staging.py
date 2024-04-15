### Dependencies ----------------------------------------------------------------
import pandas as pd # used for working with data sets
import numpy as np # used for working with arrays
import matplotlib.pyplot as plt # used for plotting
import seaborn as sns # used for plotting, see examples at https://seaborn.pydata.org/examples/index.html
import glob

import os

# Define the path to your folder containing the CSV files
folder_path = '../data'

# Create an empty dictionary to store your dataframes
dataframes = {}

# Loop through each file in the folder, load it into a dataframe, and store it in the dictionary
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)
        df_name = os.path.splitext(file_name)[0]  # Extract the filename without extension
        dataframes[df_name] = pd.read_csv(file_path)

# Optionally, you can perform operations on the dataframes here
# For example:
for df_name, df in dataframes.items():
    print(f"DataFrame {df_name}:")
    print(df.head())


print('merged_calendar_data')
print(dataframes['merged_calendar_data']['date'].min())
print(dataframes['merged_calendar_data']['date'].max())
print('calendar_9-23')
print(dataframes['calendar_9-23']['date'].min())
print(dataframes['calendar_9-23']['date'].max())
print('calendar_12-23')
print(dataframes['calendar_12-23']['date'].min())
print(dataframes['calendar_12-23']['date'].max())