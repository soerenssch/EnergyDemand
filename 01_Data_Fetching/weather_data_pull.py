import pandas as pd
import requests
import json

key = '3c1e7c92b954a643255bf4c79684fddb'

# London
lat = '51.49'
lon = '-0.12'

url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={key}"

response = requests.get(url)

file_path = 'data/custom/current_forecast_london.json'

if response.status_code == 200:
    data = response.json()
    with open(file_path, 'w') as file:
        json.dump(data, file)
else:
    print("Failed to retrieve data")

# Liverpool
lat = '53.38'
lon = '-2.98'

url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={key}"

response = requests.get(url)

file_path = 'data/custom/current_forecast_liverpool.json'

if response.status_code == 200:
    data = response.json()
    with open(file_path, 'w') as file:
        json.dump(data, file)
else:
    print("Failed to retrieve data")

# Bath
lat = '51.38'
lon = '-2.32'

url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={key}"

response = requests.get(url)

file_path = 'data/custom/current_forecast_bath.json'

if response.status_code == 200:
    data = response.json()
    with open(file_path, 'w') as file:
        json.dump(data, file)
else:
    print("Failed to retrieve data")

