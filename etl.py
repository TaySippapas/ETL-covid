import requests
import pandas as pd
import sqlite3

def fetch_covid_data():
    url = "https://disease.sh/v3/covid-19/countries"
    response = requests.get(url)
    return response.json()
def transform_data(data):
    df = pd.DataFrame(data)
    df = pd.json_normalize(data)
    # For Diamond Princess
    df.loc[df['country'] == 'Diamond Princess', 'countryInfo.iso2'] = 'DP'

    # For MS Zaandam
    df.loc[df['country'] == 'MS Zaandam', 'countryInfo.iso2'] = 'MZ'

    return df
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
        INSERT OR IGNORE INTO country (country_id, country_name, continent, population)
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
        INSERT OR IGNORE INTO country_covid_stats (cases, deaths, recovered, country_id)
        VALUES (?,?,?,?)
    """,stats_data)
    covid_daily = [
        (
            row['todayCases'],            
            row['todayDeaths'],          
            row['todayRecovered'],
            row['countryInfo.iso2']          
        )
        for _, row in df.iterrows()
    ]
    cursor.executemany("""
        INSERT OR IGNORE INTO covid_daily (todayCases, todayDeaths, todayRecovered, country_id)
        VALUES (?,?,?,?)
    """,covid_daily)

    conn.commit()
    conn.close()
    print("Data loaded successfully!")
data = fetch_covid_data()
df = transform_data(data)
load_data(df)
