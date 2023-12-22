import streamlit as st
from ElexonDataPortal import api
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta
import time
import schedule

client = api.Client(st.secrets["api_key"])

@st.cache_data
def get_time():
    return datetime.utcnow()

@st.cache_data
def fetch_market_price_data(date):
    df = client.get_MID(date.strftime("%Y-%m-%d"), date.strftime("%Y-%m-%d"))
    return df.loc[df['marketIndexDataProviderId'] == 'APXMIDP']

def refresh_market_price():
    time = get_time()
    df = fetch_market_price_data(time)

    with market_price_placeholder.container():
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Last Updated", time.strftime("%H:%M"))
        col2.metric("Spot Price (GBP/MWh)", f'{df["marketIndexPrice"].iloc[-1]} GBP')
        col3.metric("Today's High", f'{df["marketIndexPrice"].max()} GBP')
        col4.metric("Today's Low", f'{df["marketIndexPrice"].min()} GBP')

        chart = go.Figure(
            data=[go.Scatter(x=df['local_datetime'], y=df['marketIndexPrice'], mode='lines')],
            layout_yaxis_range=[0, df['marketIndexPrice'].max()],
            layout_xaxis_range=[time.strftime("%Y-%m-%d"), (time + timedelta(days=1)).strftime("%Y-%m-%d")],
            layout_yaxis_title='Spot Price in GBP per MWh',
            layout_xaxis_title='Time (UTC)'
            )
        chart.update_layout(title=f"Spot Price (GBP/MWh)", xaxis_rangeslider_visible=False)
        st.plotly_chart(chart, use_container_width=True)


st.set_page_config(page_title="UK Energy Dashboard", layout="wide", page_icon="📈")

st.title('Spot Prices')

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