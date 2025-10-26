create table if not exists country
(
    country_id text primary key,
    country_name text not null,
    continent text,
    population integer
);
create table if not exists country_covid_stats
(
    id integer primary key autoincrement,
    cases integer,
    deaths integer,
    recovered integer,
    country_id text not null,
    foreign key (country_id) references country(country_id)
);
create table if not exists covid_daily
(
    id integer primary key autoincrement,
    todayCases integer,
    todayDeaths integer,
    todayRecovered integer,
    country_id text not null,
    foreign key (country_id) references country(country_id)
);
create table if not exists covid_continent_summary as
select
    c.continent,
    sum(cs.cases) as sum_cases_per_continent,
    sum(cs.deaths) as sum_death_per_continent,
    sum(cs.recovered) as sum_recovered_per_continent
from country_covid_stats cs
join country c on c.country_id = cs.country_id
group by c.continent;