### Dependencies ----------------------------------------------------------------
import pandas as pd # used for working with data sets
import numpy as np # used for working with arrays
import matplotlib.pyplot as plt # used for plotting
import seaborn as sns # used for plotting, see examples at https://seaborn.pydata.org/examples/index.html
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import glob

# Read the combined CSV file into a DataFrame
listings = pd.read_csv(r"..\data\combined.csv")

##############################################DATA PREPARATION#############################################

#TODO WITH DATA:

# Handling values
numeric_columns = listings.select_dtypes(include=['int64', 'float64']).columns
categorical_columns = listings.select_dtypes(include=['object']).columns

# Impute missing values for numerical columns with mean
listings[numeric_columns] = listings[numeric_columns].fillna(listings[numeric_columns].mean())

# Feature selection and dropping obsolete columns
exclude_columns = ['id', 'listing_url', 'scrape_id', 'last_scraped', 'source', 'name', 'description', 'neighborhood_overview', 
                   'neighbourhood', 'picture_url', 'host_url', 'host_acceptance_rate',
                   'host_thumbnail_url', 'host_picture_url', 'neighbourhood_group_cleansed', 
                   'latitude', 'longtitude', 'calendar_updated'
                   'has_availability', 'reviews_per_month', 'amenities', 'license']
columns_to_drop = [col for col in exclude_columns if col in listings.columns]
listings = listings.drop(columns=columns_to_drop)

###### Data transformation --->:

# Convert 'price' column to numeric
listings['price'] = listings['price'].replace('[\$,]', '', regex=True).astype(float)

# Convert 'host_response_rate' column to numeric
listings['host_response_rate'] = listings['host_response_rate'].replace('[\%,]', '', regex=True).astype(float)

# Bathroom needs to be ajdusted
# Fill empty values in the 'bathrooms_text' column with '1'
listings['bathrooms_text'] = listings['bathrooms_text'].fillna('1')
# Replace "Half-bath" with "0.5" in the 'bathrooms_text' column
listings['bathrooms_text'] = listings['bathrooms_text'].replace("Half-bath", "0.5")
listings['bathrooms_text'] = listings['bathrooms_text'].replace("Private half-bath", "0.5")
listings['bathrooms_text'] = listings['bathrooms_text'].replace("Shared half-bath", "0.5 shared")
# Function to extract the number from the 'bathrooms_text' column
listings['bathrooms'] = listings['bathrooms_text'].apply(lambda x: float(x.split()[0]) if pd.notnull(x) else None)
# Create the 'bathrooms_shared' column
listings['bathrooms_shared'] = listings['bathrooms_text'].str.contains('shared').astype(int)

###### Data encoding --->:
# Encoding categorical variables
label_encoders = {}
for column in categorical_columns:
    if column in listings.columns:
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

##### TESTING MODELLING IGNORE #######

from sklearn.impute import SimpleImputer

# Handling missing values
imputer = SimpleImputer(strategy='mean')
X_train_imputed = imputer.fit_transform(X_train)
X_test_imputed = imputer.transform(X_test)

# Train the regression model
regression_model = LinearRegression()
regression_model.fit(X_train_imputed, y_train)

# Predict on the test data
y_pred = regression_model.predict(X_test_imputed)

# Plotting the actual vs predicted values
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, color='blue', label='Actual vs Predicted')

# Plotting the ideal linear relationship
plt.plot(np.unique(y_test), np.poly1d(np.polyfit(y_test, y_test, 1))(np.unique(y_test)),
         color='red', linestyle='--', label='Ideal Linear Relationship')

plt.xlabel('Actual Price')
plt.ylabel('Predicted Price')
plt.title('Actual vs Predicted Price')
plt.legend()
plt.grid(True)
plt.show()
