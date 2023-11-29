import pandas as pd
import googlemaps
from geopy.geocoders import GoogleV3

df = pd.read_csv('chicago_apartments.csv')

# Create a new DataFrame to store the updated data
new_rows = []

# create API key using googlemaps geocoding API
API_KEY = 'AIzaSyAScCshi5dAcLkJaSFcO_i9QIkcT0IUnDc'
gmaps = googlemaps.Client(key=API_KEY)

# create function to extract zipcode from a given address
def get_zipcode(address):
    try:
        # Geocode the address
        geocode_result = gmaps.geocode(address)

        # Extract the zip code from the result
        if geocode_result and 'address_components' in geocode_result[0]:
            for component in geocode_result[0]['address_components']:
                if 'postal_code' in component['types']:
                    return component['long_name']

        # Return None if no zip code found
        return None
    except Exception as e:
        print(f"Error processing address {address}: {e}")
        return None

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
new_df['Zipcode'] = new_df['Address'].apply(get_zipcode)

# Save the new DataFrame to a new CSV file
new_df.to_csv('transform_apt_data.csv', index=False)

