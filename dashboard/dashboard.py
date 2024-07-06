import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

day_df['season'] = day_df.season.astype('category')
day_df['mnth'] = day_df.mnth.astype('category')
day_df['holiday'] = day_df.holiday.astype('category')
day_df['weekday'] = day_df.weekday.astype('category')
day_df['workingday'] = day_df.workingday.astype('category')
day_df['weathersit'] = day_df.weathersit.astype('category')

day_df.season.replace((1,2,3,4), ('Winter','Spring','Summer','Fall'), inplace=True)
day_df.yr.replace((0,1), (2011,2012), inplace=True)
day_df.mnth.replace((1,2,3,4,5,6,7,8,9,10,11,12),('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'), inplace=True)
day_df.weathersit.replace((1,2,3,4), ('Clear','Misty/Cloudy','Light Rain/Snow','Heavy Rain/Snow'), inplace=True)
day_df.weekday.replace((0,1,2,3,4,5,6), ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'), inplace=True)
day_df.workingday.replace((0,1), ('No', 'Yes'), inplace=True)
day_df.holiday.replace((0,1), ('No', 'Yes'), inplace=True)

hour_df['season'] = hour_df.season.astype('category')
hour_df['yr'] = hour_df.yr.astype('category')
hour_df['mnth'] = hour_df.mnth.astype('category')
hour_df['holiday'] = hour_df.holiday.astype('category')
hour_df['weekday'] = hour_df.weekday.astype('category')
hour_df['workingday'] = hour_df.workingday.astype('category')
hour_df['weathersit'] = hour_df.weathersit.astype('category')

hour_df.season.replace((1,2,3,4), ('Winter','Spring','Summer','Fall'), inplace=True)
hour_df.yr.replace((0,1), (2011,2012), inplace=True)
hour_df.mnth.replace((1,2,3,4,5,6,7,8,9,10,11,12),('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'), inplace=True)
hour_df.weathersit.replace((1,2,3,4), ('Clear','Misty/Cloudy','Light Rain/Snow','Heavy Rain/Snow'), inplace=True)
hour_df.weekday.replace((0,1,2,3,4,5,6), ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'), inplace=True)
hour_df.workingday.replace((0,1), ('No', 'Yes'), inplace=True)
hour_df.holiday.replace((0,1), ('No', 'Yes'), inplace=True)


def create_monthly_counts(df):
    monthly_counts_df = df.groupby(by=['mnth', 'yr']).agg({
        'cnt': 'sum'
    }).reset_index()

    return monthly_counts_df

def create_season_counts(df):
    season_counts_df = df.groupby(by=['season', 'yr']).agg({
        'cnt': 'sum'
    }).reset_index()

    return season_counts_df

def create_weather_counts(df):
    weather_counts_df = df.groupby(by=['weathersit', 'yr']).agg({
        'cnt': 'sum'
    }).reset_index()

    return weather_counts_df

def create_hour_counts(df):
    hour_counts_df = df.groupby(by=['hr', 'workingday']).agg({
        'cnt': 'sum'
    }).reset_index()

    return hour_counts_df

# Sidebar for filtering
st.sidebar.title("Filters")
year_filter = st.sidebar.multiselect("Select Year", day_df['yr'].unique())
season_filter = st.sidebar.multiselect("Select Season", day_df['season'].unique())

# Apply filters
filtered_day_df = day_df.copy()
if year_filter:
    filtered_day_df = filtered_day_df[filtered_day_df['yr'].isin(year_filter)]
if season_filter:
    filtered_day_df = filtered_day_df[filtered_day_df['season'].isin(season_filter)]

filtered_hour_df = hour_df.copy()
if year_filter:
    filtered_hour_df = filtered_hour_df[filtered_hour_df['yr'].isin(year_filter)]
if season_filter:
    filtered_hour_df = filtered_hour_df[filtered_hour_df['season'].isin(season_filter)]

monthly_counts_df = create_monthly_counts(filtered_day_df)
season_counts_df = create_season_counts(filtered_day_df)
weather_counts_df = create_weather_counts(filtered_day_df)
hour_counts_df = create_hour_counts(filtered_hour_df)

custom_palette = {
    2011: 'black',
    2012: '#ECCEAE'
}

st.header('Bike Rent Dashboard')

st.subheader('Monthly Rented')

col1, col2 = st.columns(2)

with col1:
    total_rented = monthly_counts_df.cnt.sum()
    st.metric('All-time Total Rented', value=total_rented)

plt.figure(figsize=(10, 5))


sns.lineplot(
    data=monthly_counts_df,
    x='mnth',
    y='cnt',
    hue='yr',
    palette= custom_palette,
    marker='o'
)
plt.title('Trend Sewa Sepeda Tahunan')
plt.xlabel('Month')
plt.ylabel('Total Rentals')
plt.legend(title='Year', loc='upper right')
plt.tight_layout()
st.pyplot(plt.gcf())

st.subheader('Total Sewa Sepeda Setiap Musim')

plt.figure(figsize=(10, 5))

sns.barplot(
    x='season', 
    y='cnt', 
    data=season_counts_df, 
    hue='yr',
    palette=custom_palette
)

plt.xlabel("Season")
plt.ylabel("Total Rentals")
plt.title("Total Sewa Sepeda Setiap Musim")
plt.legend(title="Year", loc="upper right")
plt.tight_layout()
st.pyplot(plt.gcf())

st.subheader('Total Sewa Sepeda Berdasarkan Cuaca')

plt.figure(figsize=(10, 6))

sns.barplot(
    x='weathersit', 
    y='cnt', 
    data=weather_counts_df,
    hue='yr',
    palette=custom_palette
)

plt.xlabel("Weather")
plt.ylabel("Total Rentals")
plt.title("Total Sewa Sepeda Berdasarkan Cuaca")
plt.legend(title="Year", loc="upper right")
plt.tight_layout()
st.pyplot(plt.gcf())

st.subheader('Total Sewa Sepeda Berdasarkan Jam dan Hari Kerja')

plt.figure(figsize=(10, 5))

sns.barplot(
    x='hr', 
    y='cnt', 
    data=hour_counts_df, 
    hue='workingday',
    palette='rocket'
)

plt.xlabel("Jam")
plt.ylabel("Total Rentals")
plt.title("Total Penggunaan Sepeda Berdasarkan Jam dan Hari Kerja")
plt.tight_layout()
st.pyplot(plt.gcf())

st.caption('Copyright (c) Dicoding & Nasta 2024')