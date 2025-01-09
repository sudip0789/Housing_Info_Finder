import pandas as pd
file_path = 'data/single_family_homes_estimate.csv'
file_path2 = 'data/condo_estimate.csv'
df = pd.read_csv(file_path)
df2 = pd.read_csv(file_path2)
# Columns to keep
columns_to_keep = ['RegionName', 'RegionType', 'StateName', 'State', 'City', 'Metro', 'CountyName', '2024-11-30']

# Filter the dataframe to include only the specified columns
df = df[columns_to_keep]
df2 = df2[columns_to_keep]
# Save the modified dataframe to a new CSV file
df.to_csv('data/single_home_value_estimate.csv', index=False)
df2.to_csv('data/condos_value_estimate.csv', index=False)
