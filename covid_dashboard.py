import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

@st.cache
def fetch_data():
    df = pd.read_json('https://covidtracking.com/api/v1/us/daily.json')
    df['date'] = pd.to_datetime(df['date'], format="%Y%m%d")
    df.set_index('date', inplace=True)
    df.sort_index(ascending=True, inplace=True)
    return df

df = fetch_data()

options = {"Cumulative Positive Results": 'positive',
    "Daily Positive Tests": 'positiveIncrease',
    "Cumulative Deaths": 'death',
    "Daily Deaths": 'deathIncrease',
    "Current Hospitalizations": 'hospitalizedCurrently',
    "Daily Hospitalizations": 'hospitalizedIncrease',
    "Cumulative Hospitalizations": 'hospitalizedCumulative', 
    "Current ICU Patients": 'inIcuCurrently', 
    "Cumulative ICU Patients": 'inIcuCumulative',
    "Current Ventilator Patients": 'onVentilatorCurrently', 
    "Cumulative Ventilator Patients": 'onVentilatorCumulative', 
    "Recovered Patients": 'recovered',
    "Daily Tests Performed": 'totalTestResultsIncrease',
    "Cumulative Tests Performed": 'totalTestResults'}

## Build page
st.title('COVID-19 Dashboard: US Data')
st.subheader('Source: https://covidtracking.com')

start_date = st.sidebar.date_input("Start Date", value=datetime(2020,3,1))
end_date = st.sidebar.date_input("End Date", value=df.index.max())

charts = st.sidebar.multiselect("Select individual charts to display:",
                options=list(options.keys()),
                default=list(options.keys())[:1])

for chart in charts:
    df[options[chart]].loc[start_date : end_date + timedelta(days=1)].plot(label=chart, figsize=(8,6))
    plt.xlabel('Date')
    plt.legend(loc="upper left")
st.pyplot()