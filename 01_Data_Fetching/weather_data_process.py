import pandas as pd
import json

cities = ['london', 'liverpool', 'bath']

# Define columns for the DataFrame
columns = ['city', 'datetime', 'temp', 'temp_min', 'temp_max', 'humidity']

# Initialize an empty DataFrame
df = pd.DataFrame(columns=columns)

for city in cities:
    with open(f'00_Data/custom/current_forecast_{city}.json', 'r') as file:
        data = json.load(file)

    # Iterate over each item in the data list
    for item in data['list']:
        datetime = pd.to_datetime(item['dt'], unit='s', utc=True)
        temp = item['main']['temp']
        temp_min = item['main']['temp_min']
        temp_max = item['main']['temp_max']
        humidity = item['main']['humidity']

        # Append each observation as a new row in the DataFrame
        df = df.append({'city': city, 'datetime': datetime, 'temp': temp, 
                        'temp_min': temp_min, 'temp_max': temp_max, 
                        'humidity': humidity}, ignore_index=True)

# Save the DataFrame to CSV
df.to_csv('00_Data/custom/forecasts_combined.csv')

# Print the DataFrame
print(df)
