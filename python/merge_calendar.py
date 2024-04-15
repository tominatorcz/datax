import pandas as pd

def merge_calendar_data():
    # Read data from calendar_6-23.csv
    calendar_6_23 = pd.read_csv("../data/calendar_6-23.csv")
    # Filter records up to 16.9.2023
    calendar_6_23_filtered = calendar_6_23[calendar_6_23['date'] <= '2023-09-16']

    # Read data from calendar_9-23.csv
    calendar_9_23 = pd.read_csv("../data/calendar_9-23.csv")
    # Filter records up to 19.12.2023
    calendar_9_23_filtered = calendar_9_23[calendar_9_23['date'] <= '2023-12-19']

    # Read data from calendar_12-23.csv
    calendar_12_23 = pd.read_csv("../data/calendar_12-23.csv")

    # Concatenate all filtered dataframes with ignoring index
    merged_calendar_data = pd.concat([calendar_6_23_filtered, calendar_9_23_filtered, calendar_12_23], ignore_index=True)
    print(merged_calendar_data)

    # Sort the DataFrame first by 'listing_id' and then by 'date'
    merged_calendar_data.sort_values(by=['listing_id', 'date'], inplace=True)

    return merged_calendar_data


merged_data = merge_calendar_data()
print(merged_data)

# Save the merged data to a CSV file
merged_data.to_csv("../data/merged_calendar_data.csv", index=False)
