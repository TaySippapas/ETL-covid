from prefect import flow
from covid_etl_oltp import fetch_covid_data, transform_data, load_data
from covid_el_olap import load_to_warehouse
@flow(name="COVID ETL Pipeline")
def covid_etl_pipeline():
    data = fetch_covid_data()
    df = transform_data(data)
    load_data(df)

    load_to_warehouse()
if __name__ == "__main__":
    covid_etl_pipeline()