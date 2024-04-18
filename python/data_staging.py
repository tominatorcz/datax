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
#for df_name, df in dataframes.items():
#    print(f"DataFrame {df_name}:")
#    print(df.head())


#print('combined_calendar')
#print(dataframes['combined_calendar']['date'].min())
#print(dataframes['combined_calendar']['date'].max())


#####COMBINE LISTINGS
def combine_listings():
    # Combine the DataFrames
    combined_listings = pd.concat([dataframes["listings_detail_6-23"], dataframes["listings_detail_9-23"], dataframes["listings_detail_12-23"]])
    
    # Sort by 'last_scraped' column in descending order to ensure the newest entries are on top
    combined_listings = combined_listings.sort_values(by='last_scraped', ascending=False)
    
    # Remove duplicates based on 'listing_id', keeping the first occurrence (which will be the newest one due to sorting)
    combined_listings = combined_listings.drop_duplicates(subset='id', keep='first')
    
    # Reset the index after dropping duplicates
    combined_listings = combined_listings.reset_index(drop=True)

    return combined_listings

# Save the combined DataFrame to a new CSV file
combine_listings().to_csv('../data/merged_listings.csv', index=False)

#####COMBINE CALENDARS
import pandas as pd

def combine_calendar():
    # Filter records up to 16.9.2023
    calendar_6_23_filtered = dataframes["calendar_6-23"][dataframes["calendar_6-23"]['date'] <= '2023-09-16']

    # Filter records up to 19.12.2023
    calendar_9_23_filtered = dataframes["calendar_9-23"][dataframes["calendar_9-23"]['date'] <= '2023-12-19']

    # Concatenate all filtered dataframes with ignoring index
    combined_calendar = pd.concat([calendar_6_23_filtered, calendar_9_23_filtered, dataframes["calendar_12-23"]], ignore_index=True)

    # Sort the DataFrame first by 'listing_id' and then by 'date'
    combined_calendar.sort_values(by=['listing_id', 'date'], inplace=True)

    return combined_calendar

# Save the merged data to a CSV file
combine_calendar().to_csv("../data/merged_calendar.csv", index=False)

