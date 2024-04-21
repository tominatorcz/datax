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
