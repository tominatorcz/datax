### Dependencie ----------------------------------------------------------------
import pandas as pd # used for working with data sets
import numpy as np # used for working with arrays
import matplotlib.pyplot as plt # used for plotting
import seaborn as sns # used for plotting, see examples at https://seaborn.pydata.org/examples/index.html
import glob

# Get all file paths in the directory
file_paths = glob.glob(r"..\data\listings_detail*.csv")

# Read all CSV files into DataFrames and concatenate them
combined_df = pd.concat((pd.read_csv(file) for file in file_paths), ignore_index=True)

# Write the combined DataFrame to a new CSV file
combined_df.to_csv(r"..\data\combined.csv", index=False)