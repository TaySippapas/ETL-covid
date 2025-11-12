import os
import sqlite3
import psycopg2
from dotenv import load_dotenv
from datetime import datetime
from prefect import task


load_dotenv()
@task
def load_to_warehouse():
    # Load env
    PG_HOST = os.getenv("PG_HOST")
    PG_PORT = os.getenv("PG_PORT")
    PG_DB = os.getenv("PG_DB")
    PG_USER = os.getenv("PG_USER")
    PG_PASS = os.getenv("PG_PASS")

    # Connect to SQLite (OLTP)
    sqlite_conn = sqlite3.connect("covid_etl.db")
    sqlite_cursor = sqlite_conn.cursor()

    query = """
    SELECT 
        c.country_id,
        c.country_name,
        c.continent,
        c.population,
        d.date,
        s.cases AS total_cases,
        s.deaths AS total_deaths,
        s.recovered AS total_recovered,
        d.todayCases AS new_cases,
        d.todayDeaths AS new_deaths,
        d.todayRecovered AS new_recovered,
        cc.sum_cases_per_continent,
        cc.sum_death_per_continent,
        cc.sum_recovered_per_continent
    FROM country c
    JOIN country_covid_stats s ON c.country_id = s.country_id
    JOIN covid_daily d ON c.country_id = d.country_id
    JOIN covid_continent_summary cc ON c.continent = cc.continent
    """

    sqlite_cursor.execute(query)
    rows = sqlite_cursor.fetchall()
    sqlite_conn.close()

    snapshot = datetime.now()
    rows_with_snapshot = [row + (snapshot,) for row in rows]

    pg_conn = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        database=PG_DB,
        user=PG_USER,
        password=PG_PASS
    )
    pg_cursor = pg_conn.cursor()

    insert_query = """
    INSERT INTO covid_country_facts (
        country_id, country_name, continent, population, date,
        total_cases, total_deaths, total_recovered,
        new_cases, new_deaths, new_recovered,
        sum_cases_per_continent, sum_death_per_continent, sum_recovered_per_continent,
        snapshot_dt
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (country_id, date) DO NOTHING;
    """

    pg_cursor.executemany(insert_query, rows_with_snapshot)
    pg_conn.commit()
    pg_conn.close()

