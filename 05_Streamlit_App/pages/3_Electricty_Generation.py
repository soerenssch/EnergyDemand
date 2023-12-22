import streamlit as st
from ElexonDataPortal import api
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import schedule

client = api.Client(st.secrets["api_key"])

@st.cache_data
def get_time():
    return datetime.utcnow()

@st.cache_data
def fetch_fuel_data(date):
    df = client.get_FUELHH(date.strftime("%Y-%m-%d"), date.strftime("%Y-%m-%d"))
    return df

def refresh_market_price():
    time = get_time()
    df = fetch_fuel_data(time)
    column_names = {
        'ccgt': 'Gas',
        'oil': 'Oil',
        'coal': 'Coal',
        'nuclear': 'Nuclear',
        'wind': 'Wind',
        'npshyd': 'Hydroelectric',
        'biomass': 'Biomass'
    }

    with market_price_placeholder.container():
        df[['ccgt', 'oil', 'coal', 'nuclear', 'wind', 'npshyd', 'biomass']] = df[['ccgt', 'oil', 'coal', 'nuclear', 'wind', 'npshyd', 'biomass']].astype(int)
        total = df.iloc[-1][['ccgt', 'oil', 'coal', 'nuclear', 'wind', 'npshyd', 'biomass']].astype(int).sum()
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        col1.metric("Gas", f"{df['ccgt'].iloc[-1]/total:.1%}")
        col2.metric("Oil", f"{df['oil'].iloc[-1]/total:.1%}")
        col3.metric("Coal", f"{df['coal'].iloc[-1]/total:.1%}")
        col4.metric("Nuclear", f"{df['nuclear'].iloc[-1]/total:.1%}")
        col5.metric("Wind", f"{df['wind'].iloc[-1]/total:.1%}")
        col6.metric("Hydroelectric", f"{df['npshyd'].iloc[-1]/total:.1%}")
        col7.metric("Biomass", f"{df['biomass'].iloc[-1]/total:.1%}")

        df = df.rename(columns=column_names).melt(id_vars=['local_datetime'], value_vars=['Gas', 'Oil', 'Coal', 'Nuclear', 'Wind', 'Hydroelectric', 'Biomass'], var_name='fuel', value_name='gen')

        chart = px.line(df, x="local_datetime", y="gen", color='fuel', labels={
                     "local_datetime": "Time (UTC)",
                     "gen": "Generated Electricity in MW",
                     "fuel": "Fuel Type"
                 }, title='Generation by Fuel Type')
        chart.update_xaxes(range=[time.strftime("%Y-%m-%d"), (time + timedelta(days=1)).strftime("%Y-%m-%d")])
        st.plotly_chart(chart, use_container_width=True)


st.set_page_config(page_title="UK Energy Dashboard", layout="wide", page_icon="📈")

st.title('Electricity Generation by Fuel Type')

market_price_placeholder = st.empty()
refresh_market_price()





def refresh_data():
    st.cache_data.clear()
    refresh_market_price()

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