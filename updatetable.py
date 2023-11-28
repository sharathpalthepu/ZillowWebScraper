import pandas as pd


df = pd.read_csv('chicago_apartments.csv')

# Create a new DataFrame to store the updated data
new_rows = []

# Iterate through each row
for index, row in df.iterrows():
    # Check each bed type column and create new rows accordingly
    if row['Studio'] == "Studio":
        new_rows.append({'Address': row['Address'], 'Bed Type': 'Studio', 'Price': row['Studio Price'], 'Link': row['Links']})
    if row['1 Bed'] == "1 Bed":
        new_rows.append({'Address': row['Address'], 'Bed Type': '1 Bed', 'Price': row['1 Bed Price'], 'Link': row['Links']})
    if row['2 Bed '] == "2 Bed":
        new_rows.append({'Address': row['Address'], 'Bed Type': '2 Bed', 'Price': row['2 Bed Price'], 'Link': row['Links']})

# Create a new DataFrame with the updated rows
new_df = pd.DataFrame(new_rows)

# Save the new DataFrame to a new CSV file
new_df.to_csv('transform_apt_data.csv', index=False)

