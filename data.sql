create table country
(
    country_id text primary key,
    country_name text not null,
    continent text,
    population integer
);
create table country_covid_stats
(
    id integer primary key autoincrement,
    cases integer,
    deaths integer,
    recovered integer,
    country_id text not null,
    foreign key (country_id) references country(country_id)
);
create table covid_daily
(
    id integer primary key autoincrement,
    todayCases integer,
    todayDeaths integer,
    todayRecovered integer,
    country_id text not null,
    foreign key (country_id) references country(country_id)
)