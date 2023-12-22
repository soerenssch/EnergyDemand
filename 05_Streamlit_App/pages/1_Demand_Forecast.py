import streamlit as st
from ElexonDataPortal import api
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime, timedelta, date
import time
import schedule
import pickle
import numpy as np
from prophet import Prophet
from prophet.serialize import model_from_json
import requests
import pytz

client = api.Client(st.secrets["api_key"])

@st.cache_data
def get_time():
    return datetime.utcnow()

@st.cache_data
def fetch_demand_data():
    time = get_time()
    df = client.get_SYSDEM((time - timedelta(days=28)).strftime("%Y-%m-%d"), (time + timedelta(days=28)).strftime("%Y-%m-%d"))
    return df

@st.cache_data
def retrain_model_and_forecast():
    with open('model/prophet_serialized_model.json', 'r') as fin:
        model = model_from_json(fin.read())  # Load model
    
    df = fetch_demand_data()
    last_demand = df.loc[df['recordType'] == 'ITSDO'].iloc[-1]
    weather_df = fetch_weather_data()
    prophet_data = weather_df.tz_convert(None).reset_index().rename(columns={
        'index':'ds'
    })
    pred = model.predict(prophet_data)
    diff = float(last_demand['demand']) - pred['yhat'].loc[0]
    pred['yhat'] += diff
    return pd.Series(pred['yhat'].to_numpy(), index=weather_df.index)

@st.cache_data
def fetch_weather_data():
    locations = {
        'london': {
            'lat': 51.503655,
            'lon': -0.105732
        },
        'liverpool': {
            'lat': 53.402859,
            'lon': -2.969904
        },
        'bath': {
            'lat': 51.387535,
            'lon': -2.373896
        }
    }
    weather_dfs = []
    for key, loc in locations.items():
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={loc['lat']}&lon={loc['lon']}&appid={st.secrets['weather_key']}"
        response = requests.get(url)
        weather_data = [{
            f'datetime': datetime.fromtimestamp(x['dt'], tz=pytz.utc),
            f'temp_{key}': x['main']['temp'],
            f'pressure_{key}': x['main']['pressure'],
            f'humidity_{key}': x['main']['humidity'],
            f'wind_speed_{key}': x['wind']['speed'],
            f'clouds_all_{key}': x['clouds']['all']
        } for x in response.json()['list']]
        weather_df = pd.DataFrame(weather_data)
        weather_dfs.append(weather_df.set_index('datetime'))
        
    df_weather = pd.concat(weather_dfs, axis=1)

    df = fetch_demand_data()
    last_demand = df.loc[df['recordType'] == 'ITSDO'].iloc[-1]
    forecast_dp = 48*28
    date_index = pd.date_range(start=last_demand['local_datetime'], periods=forecast_dp+1, freq='30T')
    df_reindexed = df_weather.reindex(date_index)
    df_interpolated = df_reindexed.interpolate(method='time', fill_value="extrapolate", limit_direction="both")
    return df_interpolated


def refresh():

    time = get_time()
    df = fetch_demand_data()
    forecast_series = retrain_model_and_forecast()

    forecast_dataframe = forecast_series.to_frame(name='demand').reset_index(names='local_datetime')
    forecast_dataframe['recordType'] = 'our_forecast'

    new_df = pd.concat([df, forecast_dataframe])

    new_df['recordType'] = new_df['recordType'].replace({
        'our_forecast': 'Our Forecast',
        'ITSDO': 'Actual Demand',
        'TSDF': 'Exelon Forecast'
        })


    with market_price_placeholder.container():

        chart = px.line(new_df, x="local_datetime", y="demand", color='recordType', labels={
                     "local_datetime": "Time (UTC)",
                     "demand": "National Energy Demand in MW",
                     "recordType": "Data Source"
                 }, title='Generation by Fuel Type')
        chart.update_xaxes(range=[(time - timedelta(days=history_days)).strftime("%Y-%m-%d"), (time + timedelta(days=(forecast_days+1))).strftime("%Y-%m-%d")])
        st.plotly_chart(chart, use_container_width=True)

        st.write(f'Last Update: {get_time().strftime("%H:%M")}')


st.set_page_config(page_title="UK Energy Dashboard", layout="wide", page_icon="📈")

st.title('Demand Forecast')

st.header('Settings')

col1, col2 = st.columns(2)
with col1: 
    history_days = st.select_slider(
        'Select Number of Past Days',
        options=[0, 7, 14, 28])
with col2:
    forecast_days = st.select_slider(
        'Select Number of Forecasted Days',
        options=[0, 7, 14, 28])



market_price_placeholder = st.empty()
refresh()



def refresh_data():
    st.cache_data.clear()
    refresh()

schedule.every().hour.at(':00').do(refresh_data)
schedule.every().hour.at(':30').do(refresh_data)

while 1:
    n = schedule.idle_seconds()
    if n is None:
        # no more jobs
        break
    elif n > 0:
        # sleep exactly the right amount of time
        time.sleep(n)
    schedule.run_pending()