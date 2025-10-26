create table if not exists country
(
    country_id text primary key,
    country_name text not null,
    continent text,
    population integer
);
create table if not exists country_covid_stats
(
    country_id text primary key,
    cases integer,
    deaths integer,
    recovered integer,
    foreign key (country_id) references country(country_id)
);
create table if not exists covid_daily
(
    country_id text primary key,
    todayCases integer,
    todayDeaths integer,
    todayRecovered integer,
    date TEXT NOT NULL,
    foreign key (country_id) references country(country_id)
);
CREATE TABLE IF NOT EXISTS covid_continent_summary (
    continent TEXT PRIMARY KEY,
    sum_cases_per_continent INTEGER,
    sum_death_per_continent INTEGER,
    sum_recovered_per_continent INTEGER
);