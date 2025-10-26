from prefect import flow
from covid_etl import fetch_covid_data, transform_data, load_data

@flow(name="COVID ETL Pipeline")
def covid_etl_pipeline():
    data = fetch_covid_data()
    df = transform_data(data)
    load_data(df)

if __name__ == "__main__":
    covid_etl_pipeline()