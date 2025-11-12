import requests
import pandas as pd
import sqlite3
from prefect import task
from datetime import datetime

@task
def fetch_covid_data():
    url = "https://disease.sh/v3/covid-19/countries"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

@task
def transform_data(data):
    df = pd.json_normalize(data)
    # For Diamond Princess
    df.loc[df['country'] == 'Diamond Princess', 'countryInfo.iso2'] = 'DP'

    # For MS Zaandam
    df.loc[df['country'] == 'MS Zaandam', 'countryInfo.iso2'] = 'MZ'
    df['date'] = datetime.today().strftime('%Y-%m-%d')
    return df

@task
def load_data(df):
    conn = sqlite3.connect('covid_etl.db')
    cursor=conn.cursor()

    countries_data = [
        (
            row['countryInfo.iso2'],   
            row['country'],            
            row['continent'],          
            row['population']          
        )
        for _, row in df.iterrows()
    ]

    cursor.executemany("""
        INSERT OR REPLACE INTO country (country_id, country_name, continent, population)
        VALUES (?, ?, ?, ?)
    """, countries_data)
    stats_data = [
        (
            row['cases'],
            row['deaths'],
            row['recovered'],
            row['countryInfo.iso2']
        )
        for _, row in df.iterrows()
    ]

    cursor.executemany("""
        INSERT OR REPLACE INTO country_covid_stats (cases, deaths, recovered, country_id)
        VALUES (?,?,?,?)
    """,stats_data)
    daily_data = [
        (
            row['todayCases'], 
            row['todayDeaths'], 
            row['todayRecovered'], 
            row['countryInfo.iso2'], 
            row['date']
        )
        for _, row in df.iterrows()
    ]

    cursor.executemany("""
        INSERT OR REPLACE INTO covid_daily (todayCases, todayDeaths, todayRecovered, country_id, date)
        VALUES (?, ?, ?, ?, ?)
    """, daily_data)

    cursor.execute("DELETE FROM covid_continent_summary")
    cursor.execute("""
        INSERT INTO covid_continent_summary (continent, sum_cases_per_continent, sum_death_per_continent, sum_recovered_per_continent)
        SELECT c.continent,
               SUM(cs.cases),
               SUM(cs.deaths),
               SUM(cs.recovered)
        FROM country_covid_stats cs
        JOIN country c ON c.country_id = cs.country_id
        GROUP BY c.continent
    """)

    conn.commit()
    conn.close()
    print("Data loaded successfully!")

