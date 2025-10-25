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
def load_data(data):
    return
data = fetch_covid_data()
df = transform_data(data)

