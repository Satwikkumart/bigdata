from pandas_profiling import ProfileReport
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as style
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")
# Load the data from a file
accidents = pd.read_csv('accidents.csv')
# Display the first few rows of the dataset
accidents.head()

# Load the data from a file
bikers = pd.read_csv('bikers.csv')

# Display the first few rows of the dataset
bikers.head()

# Merge the DataFrames on the "Accident_Index" column
merged_df = bikers.merge(accidents, on='Accident_Index')

# Display the merged DataFrame
merged_df.head()

merged_df['Date'] = pd.to_datetime(merged_df['Date'])

filtered_merged_df = merged_df[merged_df['Date'] > pd.to_datetime('1990-01-01')]

# Generate the profile report
profile = ProfileReport(filtered_merged_df)

# Save the report as an HTML file
profile.to_file("data_profile_report_filtered.html")

# Check for null values in each column
null_counts = filtered_merged_df.isnull().sum()

# Display the null counts for each column
print(null_counts)

# Step 1: Remove outliers
filtered_merged_df = filtered_merged_df[(filtered_merged_df['Speed_limit'] > 0) & (filtered_merged_df['Speed_limit'] <= 100)]

# Step 2: Convert speed limit to integer
filtered_merged_df['Speed_limit'] = filtered_merged_df['Speed_limit'].astype(int)

# Step 3: Round speed limit values
filtered_merged_df['Speed_limit'] = (filtered_merged_df['Speed_limit'] // 10) * 10

# Display the cleaned
filtered_merged_df['Speed_limit'].value_counts()


# Standardize values

filtered_merged_df['Road_conditions'] = filtered_merged_df['Road_conditions'].replace({
    'Missing Data': 'Unknown',
    'Frost': 'Snow'
})

filtered_merged_df['Road_conditions'].value_counts()

# Standardize values

filtered_merged_df['Weather_conditions'] = filtered_merged_df['Weather_conditions'].replace({
    'Clear and windy': 'Clear/Windy',
    'Rain and windy': 'Rain/Windy',
    'Snow and windy': 'Snow/Windy',
    'Missing data': 'Unknown',
    'Other': 'Unknown'
})

filtered_merged_df['Weather_conditions'].value_counts()


filtered_merged_df['Time'] = pd.to_datetime(filtered_merged_df['Time'])

# Extract the hour component from the accident_time column
filtered_merged_df['hour'] = filtered_merged_df['Time'].dt.hour

# Classify the time of accident based on the hour
filtered_merged_df['time_of_day'] = pd.cut(filtered_merged_df['hour'],
                                   bins=[0, 6, 12, 18, 24],
                                   labels=['Night', 'Morning', 'Afternoon', 'Evening'],
                                   right=False)

# Drop the 'hour' column if not needed
filtered_merged_df.drop('hour', axis=1, inplace=True)

output_path = 'output.csv'
filtered_merged_df.to_csv(output_path)