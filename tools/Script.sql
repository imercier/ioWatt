CREATE TABLE EnergyHistory
(
    timestamp timestamp NOT NULL PRIMARY key unique,
    energyProduced numeric NOT NULL,
    isValid boolean NOT NULL
);
ALTER TABLE EnergyHistory add column isValid boolean;
CREATE UNIQUE INDEX timeIndex ON EnergyHistory ("timestamp");

select  count(*) from EnergyHistory;
select  * from EnergyHistory;

CREATE USER reader WITH PASSWORD 'foo';
GRANT CONNECT ON DATABASE postgres to reader;
GRANT USAGE ON SCHEMA public to reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public to reader;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO reader;

SELECT
DATE_TRUNC('day',timestamp) AS currentday,
sum(energyProduced) as energyProducedDaily
FROM EnergyHistory
GROUP BY currentday
order by currentday;

SELECT * FROM EnergyHistory ORDER BY timestamp DESC LIMIT 10;

SELECT count(*)
FROM EnergyHistory
where
isvalid is false
AND (extract('hour' from timestamp) >= 7 AND extract('hour' from timestamp) < 21);
