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
  1.  `011_Live_Weather_Data.ipynb` - Live fetching of the energy demand and weather data for our streamlit app.
  2.  `012_Historic_Energy_Demand.ipynb` - Fetching of historic energy demand for model training. 
  3.  `secret_energy_demand.py` - secret file for energy demand API-key.
  4.  `secret_weather.py` - secret file for weather API-key.
  5.  `weather_data_pull.py` - Script to pull weather data from the OpenWeatherMap API. (initial version)
  6.  `weather_data_process.py` - Script for processing the raw weather data. (initial version)

02 - Data Pre-processing
  1. `022_Merge_Weather_and_Demand.ipynb` - Merging our key historical data for training and benchmarking.
  2. `data_handling.ipynb` - Primary notebook for initial data processing and handling. For initial Modelling purpose, not used further in our benchmarking and App.

03 - Data exploration
  1. `data_exploration.ipynb` - Data exploration and time series analytics, to gain understanding of the data structure.

04 - Model Benchmarking

`040_benchmarking_setup.ipynb` - Definition of our setup for benchmarking different ML models. 
  1. `041_bm_exponential_smoothing.ipynb` - Exponentential smoothing model (univariate) benchmark.
  2. `042_bm_XGB.ipynb` - XGB model (multivariate) benchmark. 
  3. `043_bm_ARIMA.ipynb` - ARIMA model (univariate) benchmark. 
  4. `044_bm_SARIMAX.ipynb` - SARIMAX model (multivariate) benchmark.
  5. `045_bm_mstl.ipynb` - Multiseasonal Timeseries decomposition for complex time series approaches.
  6. `046_bm_decomposed.ipynb` - Combined approach using ARIMA, XGB and NAIVE forecasting. 
  7. `047_bm_prophet_uni.ipynb` - Prophet model (univariate) benchmark. 
  8. `048_bm_prophet_multi.ipynb` - Prophet model (multivariate) benchmark.
  9. `049_bm_prophet_multi_tune.ipynb` - Tuned Prophet model (multivariate) benchmark.

05 - App development

---

## Installation
To set up this project, clone the repository and install the required dependencies:
```bash
git clone <repository-url>
cd <repository-name>
pip install [dependencies]
```

---

## Miscellaneous 

App link:
- https://ukenergy.streamlit.app/Demand_Forecast 

Data sources:
- Historic Energy Demand Data - https://www.nationalgrideso.com/data-portal/historic-demand-data/historic_demand_data_2023
- Historic Weather Data - https://openweathermap.org/history-bulk
- Real-time Weather Data - https://openweathermap.org/api

