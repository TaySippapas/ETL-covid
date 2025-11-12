from datetime import timedelta
from covid_flow import covid_etl_pipeline

if __name__ == "__main__":
    covid_etl_pipeline.serve(
        name="daily-covid-etl",
        interval=timedelta(days=1)
    )