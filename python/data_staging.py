### Dependencies ----------------------------------------------------------------
import pandas as pd # used for working with data sets
import ast
import numpy as np # used for working with arrays
import matplotlib.pyplot as plt # used for plotting
import seaborn as sns # used for plotting, see examples at https://seaborn.pydata.org/examples/index.html
from datetime import datetime
from transformers import pipeline
import time

import os

# Define the path to your folder containing the CSV files
folder_path = '../data'
# folder_path = 'data'

# Create an empty dictionary to store your dataframes
dataframes = {}

# Loop through each file in the folder, load it into a dataframe, and store it in the dictionary
for file_name in os.listdir(folder_path):
    if file_name != 'combined.csv' and file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)
        df_name = os.path.splitext(file_name)[0]  # Extract the filename without extension
        dataframes[df_name] = pd.read_csv(file_path)

##### COMBINE LISTINGS
def combine_listings():
    # Combine the DataFrames
    combined_listings = pd.concat([dataframes["listings_detail_6-23"], dataframes["listings_detail_9-23"]])
    
    # Sort by 'last_scraped' column in descending order to ensure the newest entries are on top
    combined_listings = combined_listings.sort_values(by='last_scraped', ascending=False)
    
    # Remove duplicates based on 'listing_id', keeping the first occurrence (which will be the newest one due to sorting)
    combined_listings = combined_listings.drop_duplicates(subset='id', keep='first')
    
    # Reset the index after dropping duplicates
    combined_listings = combined_listings.reset_index(drop=True)

    # Feature selection and dropping obsolete columns
    # !amenities removed
    include_columns = ['id', 'description', 'neighborhood_overview', 'host_since', 'host_about',
                       'host_is_superhost', 'host_has_profile_pic', 'host_identity_verified','neighbourhood_cleansed',
                       'room_type', 'accommodates', 'bathrooms_text', 'bedrooms', 'beds', 
                       'number_of_reviews', 'review_scores_rating', 'instant_bookable']
    columns_to_drop = [col for col in combined_listings.columns if col not in include_columns]
    combined_listings = combined_listings.drop(columns=columns_to_drop)

    return combined_listings

##### TRANSFORM LISTINGS
def listings_transformation():
    listings = combine_listings()

    ### description
    # replace not null values with words count
    listings['description'] = listings[listings['description'].notnull()]['description'].str.split().str.len()
    # replace null values with 0
    listings['description'].fillna(0, inplace=True)
    # Define bins and labels
    bins = [-1, 0, 50, 100, 150, 200, float('inf')]
    labels = [0, 1, 2, 3, 4, 5]
    # Apply the bins and labels to the description column
    # Create description_bins column
    listings['description_bins'] = pd.cut(listings['description'], bins=bins, labels=labels, include_lowest=True)
    listings['description'] = listings['description_bins']

    ### neighborhood_overview
    # Replace non-null values with 1
    listings['neighborhood_overview_bins'] = listings['neighborhood_overview'].notnull().astype(int)
    # Replace null values with 0
    listings['neighborhood_overview_bins'].fillna(0, inplace=True)
    listings['neighborhood_overview'] = listings['neighborhood_overview_bins']

    ### neighbourhood_cleansed
    # Define the mapping dictionary
    mapping_dict = {
        'Běchovice': 'Prague-outskirts',
        'Benice': 'Prague-outskirts',
        'Březiněves': 'Prague-outskirts',
        'Čakovice': 'Prague-outskirts',
        'Ďáblice': 'Prague-outskirts',
        'Dolní Chabry': 'Prague-outskirts',
        'Dolní Měcholupy': 'Prague-outskirts',
        'Dolní Počernice': 'Prague-outskirts',
        'Dubeč': 'Prague-outskirts',
        'Klánovice': 'Prague-outskirts',
        'Koloděje': 'Prague-outskirts',
        'Kolovraty': 'Prague-outskirts',
        'Královice': 'Prague-outskirts',
        'Křeslice': 'Prague-outskirts',
        'Kunratice': 'Prague-outskirts',
        'Libuš': 'Prague-outskirts',
        'Lipence': 'Prague-outskirts',
        'Lochkov': 'Prague-outskirts',
        'Lysolaje': 'Prague-outskirts',
        'Nebušice': 'Prague-outskirts',
        'Nedvězí': 'Prague-outskirts',
        'Petrovice': 'Prague-outskirts',
        'Praha 1': 'Prague-center',
        'Praha 10': 'Prague',
        'Praha 11': 'Prague',
        'Praha 12': 'Prague-outskirts',
        'Praha 13': 'Prague-outskirts',
        'Praha 14': 'Prague',
        'Praha 15': 'Prague-outskirts',
        'Praha 16': 'Prague-outskirts',
        'Praha 17': 'Prague-outskirts',
        'Praha 18': 'Prague',
        'Praha 19': 'Prague-outskirts',
        'Praha 2': 'Prague-center',
        'Praha 20': 'Prague-outskirts',
        'Praha 21': 'Prague-outskirts',
        'Praha 22': 'Prague-outskirts',
        'Praha 3': 'Prague',
        'Praha 4': 'Prague',
        'Praha 5': 'Prague',
        'Praha 6': 'Prague',
        'Praha 7': 'Prague',
        'Praha 8': 'Prague',
        'Praha 9': 'Prague',
        'Přední Kopanina': 'Prague-outskirts',
        'Řeporyje': 'Prague-outskirts',
        'Satalice': 'Prague-outskirts',
        'Šeberov': 'Prague-outskirts',
        'Slivenec': 'Prague-outskirts',
        'Štěrboholy': 'Prague-outskirts',
        'Suchdol': 'Prague-outskirts',
        'Troja': 'Prague-outskirts',
        'Újezd': 'Prague-outskirts',
        'Velká Chuchle': 'Prague-outskirts',
        'Vinoř': 'Prague-outskirts',
        'Zbraslav': 'Prague-outskirts',
        'Zličín': 'Prague-outskirts'
    }

    # Map the group to neighourhoods
    listings['neighbourhood_group'] = listings['neighbourhood_cleansed'].map(mapping_dict)
    listings['neighbourhood_cleansed'] = listings['neighbourhood_group']

    ### host_since
    # Convert 'host_since' column to datetime
    listings['host_since'] = pd.to_datetime(listings['host_since'], format='%Y-%m-%d')
    # Calculate time difference from today
    today = datetime.today()
    listings['time_difference'] = (today - listings['host_since']).dt.days
    # Convert time difference to years
    listings['years_from_today'] = listings['time_difference'] / 365
    # Create bins
    listings['host_since_bins'] = pd.cut(listings['years_from_today'], bins=[-float("inf"), 1, float("inf")], labels=[0, 1])
    # Drop intermediate columns if needed
    listings.drop(['time_difference', 'years_from_today'], axis=1, inplace=True)
    listings['host_since'] = listings['host_since_bins']

    ### host_about
    # Replace non-null values with 1
    listings['host_about_bins'] = listings['host_about'].notnull().astype(int)
    # Replace null values with 0
    listings['host_about_bins'].fillna(0, inplace=True)
    listings['host_about'] = listings['host_about_bins']
    
    ### host_response_rate
    ## Convert 'host_response_rate' column to numeric
    #listings['host_response_rate'] = listings['host_response_rate'].replace('[\%,]', '', regex=True).astype(float)
    ## Convert 'host_response_rate' float
    #listings['host_response_rate'] = listings['host_response_rate'].replace(',', '.').astype(float)
    ## Replace 'N/A' and '0' with 0
    #listings['host_response_rate'] = listings['host_response_rate'].replace(["N/A", "0"], 0)
    ## Define bin edges and labels
    #bin_edges = [-float("inf"), 0.50, 0.90, float("inf")]
    #bin_labels = [0, 1, 2]
    ## Create bins
    #listings['response_rate_bins'] = pd.cut(listings['host_response_rate'], bins=bin_edges, labels=bin_labels, right=False)
    #listings['host_response_rate'] = listings['response_rate_bins']

    ### host_is_superhost
    # Fill empty values with "f"
    listings['host_is_superhost'].fillna(value='f', inplace=True)
    # Create boolean column, t=1, f=0
    listings['host_is_superhost_bool'] = listings['host_is_superhost'].map({'t': 1, 'f': 0})
    listings['host_is_superhost'] = listings['host_is_superhost_bool']

    ### host_has_profile_pic
    # Create boolean column, t=1, f=0
    listings['host_has_profile_pic_bool'] = listings['host_has_profile_pic'].map({'t': 1, 'f': 0})
    listings['host_has_profile_pic'] = listings['host_has_profile_pic_bool']

    ### host_identity_verified
    # Create boolean column, t=1, f=0
    listings['host_identity_verified_bool'] = listings['host_identity_verified'].map({'t': 1, 'f': 0})
    listings['host_identity_verified'] = listings['host_identity_verified_bool']

    ### bathrooms_text
    # Fill empty values with '1'
    listings['bathrooms_text'] = listings['bathrooms_text'].fillna("1")
    # Replace "Half-bath" with "0.5"
    listings['bathrooms_text'] = listings['bathrooms_text'].replace("Half-bath", "0.5")
    listings['bathrooms_text'] = listings['bathrooms_text'].replace("Private half-bath", "0.5")
    listings['bathrooms_text'] = listings['bathrooms_text'].replace("Shared half-bath", "0.5 shared")
    # Function to extract the number from the 'bathrooms_text' column
    listings['bathrooms_num'] = listings['bathrooms_text'].apply(lambda x: float(x.split()[0]) if pd.notnull(x) else None)
    listings['bathrooms_num']
    # Create the 'bathrooms_shared' column
    listings['bathrooms_shared_bool'] = listings['bathrooms_text'].str.contains('shared').astype(int)

    ### bedrooms
    # Fill empty values with '1'
    listings['bedrooms'] = listings['bedrooms'].fillna(1)

    ### beds
    # Fill empty values with '1'
    listings['beds'] = listings['beds'].fillna(1)
    
    ### amenities - too many individual values
    ## Convert string representation of list to actual list
    #listings['amenities'] = listings['amenities'].apply(ast.literal_eval)
    ## Convert each cell in the 'amenities' column to a list and flatten all lists
    #all_amenities = [item for sublist in listings['amenities'] for item in sublist]
    #all_amenities
    #listings['amenities'] 
    ## Remove duplicates by converting to a set
    #unique_amenities = set(all_amenities)
    ## Convert back to a list if needed
    #unique_amenities_list = list(unique_amenities)
    #print(unique_amenities_list)
    ## Create a dataframe from the unique amenities list
    #amenities_df = pd.DataFrame(unique_amenities_list, columns=['Amenity'])
    ## Write the dataframe to a CSV file with encoding specified
    #amenities_df.to_csv('unique_amenities.csv', index=False, encoding='utf-8')

    ### instant_bookable
    # Create boolean column, t=1, f=0
    listings['instant_bookable_bool'] = listings['instant_bookable'].map({'t': 1, 'f': 0})
    listings['instant_bookable'] = listings['instant_bookable_bool']

    ### review_scores_rating
    #Replace missing values with the mean of non-missing values
    mean_rating = listings['review_scores_rating'].mean()
    listings['review_scores_rating'] = listings['review_scores_rating'].fillna(mean_rating)

    return listings


##### COMBINE CALENDARS
def combine_calendar():
    # Filter records up to 16.9.2023
    calendar_6_23_filtered = dataframes["calendar_6-23"][dataframes["calendar_6-23"]['date'] <= '2023-09-16']

    # Concatenate all filtered dataframes with ignoring index
    combined_calendar = pd.concat([calendar_6_23_filtered, dataframes["calendar_9-23"]], ignore_index=True)

    # Sort the DataFrame first by 'listing_id' and then by 'date'
    combined_calendar.sort_values(by=['listing_id', 'date'], inplace=True)

    # Feature selection and dropping obsolete columns
    include_columns_cal = ['listing_id', 'date', 'price']
    columns_to_drop_cal = [col for col in combined_calendar.columns if col not in include_columns_cal]
    combined_calendar = combined_calendar.drop(columns=columns_to_drop_cal)

    ## Clean the price column
    # Remove '$'
    combined_calendar['price'] = combined_calendar['price'].str.replace('$', '')
    # Remove commas  
    combined_calendar['price'] = combined_calendar['price'].str.replace(',', '')
    # Convert to float (or int if needed)
    combined_calendar['price'] = combined_calendar['price'].astype(float)

    # Create a boxplot of the price column
    #plt.figure(figsize=(8, 6))
    #plt.boxplot(combined_calendar['price'])
    #plt.xlabel('Price')
    #plt.ylabel('Distribution')
    #plt.title('Boxplot of Price')
    #plt.show()

    ## Remove outliers
    # Calculate lower and upper thresholds based on percentiles
    lower_threshold = combined_calendar['price'].quantile(0.01)
    upper_threshold = combined_calendar['price'].quantile(0.96)
    # Filter the DataFrame to keep only the rows within the specified quantiles
    combined_calendar = combined_calendar[
    (combined_calendar['price'] >= lower_threshold) &
    (combined_calendar['price'] <= upper_threshold)]
    
    # Change date to datetime
    combined_calendar['date'] = pd.to_datetime(combined_calendar['date'])
    
    # Adding columns for following group by operations
    combined_calendar['year'] = combined_calendar['date'].dt.year
    combined_calendar['month'] = combined_calendar['date'].dt.month
    
    # Group by 'listing_id', 'year', and 'month' and calculate the average of the 'price'
    grouped_calendar = combined_calendar.groupby(['listing_id', 'year', 'month'])['price'].mean().reset_index()

    # Rename the 'price' column to 'average_price' to reflect the aggregation
    grouped_calendar.rename(columns={'price': 'avg_price'}, inplace=True)
    
    # Date column based on year and month = output is firts date in month
    grouped_calendar['date'] = pd.to_datetime(grouped_calendar['year'].astype(str) + '-' + grouped_calendar['month'].astype(str) + '-01')
    
    return grouped_calendar

##### JOIN LISTINGS TO CALENDAR
def combine_calendar_listings():
    combined_listings = listings_transformation()
    combined_calendar = combine_calendar()

    # Select only the first 100 rows from combined_calendar
    #combined_calendar_head = combined_calendar.head(200000)
    
    # Runs right join on calendar from listings
    combined_calendar_listings = pd.merge(combined_listings, combined_calendar, how='right', left_on='id', right_on='listing_id')

    return combined_calendar_listings

##### CLEAN COMBINED FILE
def clean_calendar_listings():
    combined_data = combine_calendar_listings()
    # Obsolete columns to drop
    clean_combined_data = combined_data.drop(columns=['listing_id', 'id', 'description_bins', 'host_since_bins',
                                                      'neighborhood_overview_bins', 'neighbourhood_group', 
                                                      'host_about_bins', 'host_is_superhost_bool', 
                                                      'host_has_profile_pic_bool', 'host_identity_verified_bool',
                                                      'bathrooms_text', 'instant_bookable_bool'])
    # Convert date column to datetime type
    # clean_combined_data['date'] = pd.to_datetime(clean_combined_data['date'])

    # Sort DataFrame by the "date" column
    clean_combined_data_sorted = clean_combined_data.sort_values(by='date')

    # Group the data by neighborhood_cleansed and calculate the average price
    avg_price_per_neighbourhood = clean_combined_data.groupby('neighbourhood_cleansed')['avg_price'].mean().sort_values()

    # Create a bar plot
    #plt.figure(figsize=(12, 8))
    #avg_price_per_neighbourhood.plot(kind='bar', color='skyblue')
    #plt.xlabel('Neighborhood')
    #plt.ylabel('Average Price')
    #plt.title('Average Price per Neighborhood')
    #plt.xticks(rotation=45, ha='right')
    #plt.tight_layout()
    #plt.show()

    return clean_combined_data_sorted

##### EXPORT FILE to PICKLE
#clean_calendar_listings().to_pickle('../data/combined.pickle')


##### EXPORT FILE to CSV
clean_calendar_listings().to_csv("../data/combined.csv", index=False)


