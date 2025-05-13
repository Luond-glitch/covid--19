import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
 #loading covid data from our world Data

url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
filename = 'owid-covid-data.csv'

# Download with streaming
with requests.get(url, stream=True) as r:
    r.raise_for_status()
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

# Load into DataFrame
df = pd.read_csv(filename)

#Preview the Dataset
df.head()

#Filter Relevant Columns
df_filtered = df[['location', 'date', 'total_cases', 'total_deaths', 'new_cases', 'new_deaths', 'continent']]
df_filtered['date'] = pd.to_datetime(df_filtered['date'])
df_filtered.dropna(subset=['continent'], inplace=True)
df_filtered.head()

#Global Overview (Latest Data)
latest_date = df_filtered['date'].max()
latest_data = df_filtered[df_filtered['date'] == latest_date]

global_stats = latest_data.groupby('continent')[['total_cases', 'total_deaths']].sum().reset_index()

plt.figure(figsize=(10, 5))
sns.barplot(data=global_stats, x='continent', y='total_cases')
plt.title('Total COVID-19 Cases by Continent (Latest)')
plt.ylabel('Total Cases')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Time-Series Plot for a Country (e.g. Kenya)
kenya_data = df_filtered[df_filtered['location'] == 'Kenya']

plt.figure(figsize=(10, 5))
plt.plot(kenya_data['date'], kenya_data['total_cases'], label='Total Cases')
plt.plot(kenya_data['date'], kenya_data['total_deaths'], label='Total Deaths')
plt.title('COVID-19 Trend in Kenya')
plt.xlabel('Date')
plt.ylabel('Count')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

#Daily Cases by Continent
continent_daily = df_filtered.groupby(['date', 'continent'])['new_cases'].sum().reset_index()

plt.figure(figsize=(12, 6))
sns.lineplot(data=continent_daily, x='date', y='new_cases', hue='continent')
plt.title('Daily New COVID-19 Cases by Continent')
plt.xlabel('Date')
plt.ylabel('New Cases')
plt.tight_layout()
plt.show()
