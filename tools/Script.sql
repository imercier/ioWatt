CREATE TABLE EnergyHistory
(
    timestamp timestamp NOT NULL PRIMARY key unique,
    energyProduced numeric NOT NULL,
    isValid boolean NOT NULL
);
CREATE TABLE sunEphemeride
(
    day date NOT NULL PRIMARY key unique,
    sunrise timestamp NOT NULL,
    sunset timestamp NOT NULL,
    locationName varchar(32) NOT NULL
);

ALTER TABLE EnergyHistory add column isValid boolean;
CREATE UNIQUE INDEX timeIndex ON EnergyHistory ("timestamp");

select  count(*) from EnergyHistory;
select  * from EnergyHistory;
select  * from sunEphemeride;

CREATE USER reader WITH PASSWORD 'foo';
GRANT CONNECT ON DATABASE postgres to reader;
GRANT USAGE ON SCHEMA public to reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public to reader;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO reader;


CREATE USER grafanareader WITH PASSWORD 'password';
GRANT USAGE ON SCHEMA schema TO grafanareader;
GRANT SELECT ON schema.table TO grafanareader;

SELECT
DATE_TRUNC('day',timestamp) AS currentday,
sum(energyProduced) as energyProducedDaily
FROM EnergyHistory
GROUP BY currentday
order by currentday desc;

SELECT
ROUND((sum(energyProduced) * 0.00017)) as cash
FROM EnergyHistory;

SELECT * FROM EnergyHistory ORDER BY timestamp DESC LIMIT 10;

select distinct(DATE_TRUNC('day',timestamp)) AS startDay 
from EnergyHistory
where  energyProduced > 0
group by startDay
order by startDay asc;

select count(distinct(DATE_TRUNC('day',timestamp))) 
from EnergyHistory
where  energyProduced > 0;

SELECT
ROUND((sum(energyProduced) * 0.00017) /
(select count(distinct(DATE_TRUNC('day',timestamp))) from EnergyHistory where  energyProduced > 0), 1)
FROM energyhistory

SELECT count(*)
FROM EnergyHistory
where
isvalid is false
AND (extract('hour' from timestamp) >= 7 AND extract('hour' from timestamp) < 21);


select * 
FROM energyhistory;

select count(*) 
FROM energyhistory
where energyProduced = 0
and now() > (SELECT sunrise AT TIME ZONE 'Europe/Paris' FROM sunephemeride WHERE day = current_date)
and now() < (SELECT sunset AT TIME ZONE 'Europe/Paris' FROM sunephemeride WHERE day = current_date)
and current_date = (SELECT "day" AT TIME ZONE 'Europe/Paris' FROM sunephemeride);


select count(*) 
FROM energyhistory
where energyProduced = 0;

select
"day",
"sunrise" AT TIME ZONE 'Europe/Paris' as sunrise,
"sunset" AT TIME ZONE 'Europe/Paris' as sunset
from sunEphemeride
where current_date = "day";

select current_date