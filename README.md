# Energy Demand

This project was conducted during the course "Business Analytics and Data Science Applications". 
Our goal is to provide energy traders with information, so they can make informed decisions and match supply and demand in the energy market. 

Our approach uses historic weather and energy demand data from the UK, ranging from 2018 to 2023. 

---

## Repo Structure

00 - Data
  1.  `custom` - Data structures created by various python scripts that run when executing the app
  2.  `external` - Historical data that is not fetched live and was retrieved from various outside sources. 

01 - Data Fetching
  1.  `weather_data_pull.py` - Script to pull weather data from the OpenWeatherMap API.
  2.  `weather_data_process.py` - Script for processing the raw weather data.

02 - Data Pre-processing
  1. `data_handling.ipynb` - Primary notebook for initial data processing and handling.

Data exploration

Model Benchmarking

App development

---

## Installation
To set up this project, clone the repository and install the required dependencies:
```bash
git clone <repository-url>
cd <repository-name>
pip install -r requirements.txt
```

---

## Miscellaneous 

App link:
xx

Data sources:
- Historic Energy Demand Data - https://www.nationalgrideso.com/data-portal/historic-demand-data/historic_demand_data_2023
- Historic Weather Data - https://openweathermap.org/history-bulk
- Real-time Weather Data - https://openweathermap.org/api

API link:
XX

