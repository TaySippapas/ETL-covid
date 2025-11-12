CREATE TABLE IF NOT EXISTS covid_country_facts (
    country_id TEXT,
    country_name TEXT,
    continent TEXT,
    population INTEGER,
    date TEXT NOT NULL,
    total_cases INTEGER,
    total_deaths INTEGER,
    total_recovered INTEGER,
    new_cases INTEGER,
    new_deaths INTEGER,
    new_recovered INTEGER,
    sum_cases_per_continent INTEGER,
    sum_death_per_continent INTEGER,
    sum_recovered_per_continent INTEGER,
    PRIMARY KEY (country_id, date)
);
