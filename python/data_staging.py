### Dependencies ----------------------------------------------------------------
import pandas as pd # used for working with data sets
import numpy as np # used for working with arrays
import matplotlib.pyplot as plt # used for plotting
import seaborn as sns # used for plotting, see examples at https://seaborn.pydata.org/examples/index.html

import os

# Define the path to your folder containing the CSV files
folder_path = '../data'

# Create an empty dictionary to store your dataframes
dataframes = {}

# Loop through each file in the folder, load it into a dataframe, and store it in the dictionary
for file_name in os.listdir(folder_path):
    if file_name != 'combined.csv' and file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)
        df_name = os.path.splitext(file_name)[0]  # Extract the filename without extension
        dataframes[df_name] = pd.read_csv(file_path)

# Optionally, you can perform operations on the dataframes here
# For example:
# for df_name, df in dataframes.items():
#    print(f"DataFrame {df_name}:")
#    print(df.head())

##### COMBINE LISTINGS
def combine_listings():
    # Combine the DataFrames
    combined_listings = pd.concat([dataframes["listings_detail_6-23"], dataframes["listings_detail_9-23"], dataframes["listings_detail_12-23"]])
    
    # Sort by 'last_scraped' column in descending order to ensure the newest entries are on top
    combined_listings = combined_listings.sort_values(by='last_scraped', ascending=False)
    
    # Remove duplicates based on 'listing_id', keeping the first occurrence (which will be the newest one due to sorting)
    combined_listings = combined_listings.drop_duplicates(subset='id', keep='first')
    
    # Reset the index after dropping duplicates
    combined_listings = combined_listings.reset_index(drop=True)

    # Feature selection and dropping obsolete columns
    include_columns = ['id', 'description', 'neighborhood_overview', 'host_since', 'host_about', 'host_response_rate',
                       'host_is_superhost', 'host_total_listings_count', 'host_has_profile_pic', 'host_identity_verified',
                       'neighbourhood_cleansed', 'room_type', 'accommodates', 'bathrooms_text', 'bedrooms', 'beds',
                       'amenities', 'number_of_reviews', 'review_scores_rating', 'instant_bookable']
    columns_to_drop = [col for col in combined_listings.columns if col not in include_columns]
    combined_listings = combined_listings.drop(columns=columns_to_drop)

    return combined_listings

##### TRANSFORM LISTINGS
def listings_transformation():
    combined_listings = combine_listings()

    ### description

    ### neighborhood_overview

    ### host_since

    ### host_about

    ### host_response_rate
    # Convert 'host_response_rate' column to numeric
    combined_listings['host_response_rate'] = combined_listings['host_response_rate'].replace('[\%,]', '', regex=True).astype(float)

    ### host_is_superhost

    ### host_total_listings_count

    ### host_has_profile_pic

    ### host_identity_verified

    ### bathrooms_text
    # Fill empty values in the 'bathrooms_text' column with '1'
    combined_listings['bathrooms_text'] = combined_listings['bathrooms_text'].fillna('1')
    # Replace "Half-bath" with "0.5" in the 'bathrooms_text' column
    combined_listings['bathrooms_text'] = combined_listings['bathrooms_text'].replace("Half-bath", "0.5")
    combined_listings['bathrooms_text'] = combined_listings['bathrooms_text'].replace("Private half-bath", "0.5")
    combined_listings['bathrooms_text'] = combined_listings['bathrooms_text'].replace("Shared half-bath", "0.5 shared")
    # Function to extract the number from the 'bathrooms_text' column
    combined_listings['bathrooms'] = combined_listings['bathrooms_text'].apply(lambda x: float(x.split()[0]) if pd.notnull(x) else None)
    # Create the 'bathrooms_shared' column
    combined_listings['bathrooms_shared'] = combined_listings['bathrooms_text'].str.contains('shared').astype(int)

    ### bedrooms

    ### beds

    ### amenities

    ### instant_bookable


    return combined_listings

##### COMBINE CALENDARS
def combine_calendar():
    # Filter records up to 16.9.2023
    calendar_6_23_filtered = dataframes["calendar_6-23"][dataframes["calendar_6-23"]['date'] <= '2023-09-16']

    # Concatenate all filtered dataframes with ignoring index
    combined_calendar = pd.concat([calendar_6_23_filtered, dataframes["calendar_9-23"]], ignore_index=True)

    # Sort the DataFrame first by 'listing_id' and then by 'date'
    combined_calendar.sort_values(by=['listing_id', 'date'], inplace=True)

    return combined_calendar

##### JOIN LISTINGS TO CALENDAR
def combine_calendar_listings():
    combined_listings = listings_transformation()
    combined_calendar = combine_calendar()
    # Select only the first 100 rows from combined_calendar
    combined_calendar_head = combined_calendar.head(500)
    
    combined_calendar_listings = pd.merge(combined_calendar_head, combined_listings, how='left', left_on='listing_id', right_on='id')

    return combined_calendar_listings


combine_calendar_listings().to_csv("../data/combined.csv", index=False)


# Save the merged data to a CSV file
#combine_calendar().to_csv("../data/merged_calendar.csv", index=False)

