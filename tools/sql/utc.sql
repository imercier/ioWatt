CREATE OR REPLACE FUNCTION cast_datetime(text)
  RETURNS timestamptz AS
$$SELECT to_timestamp($1, 'YYYY-MM-DD HH24:MI:SS')$$
  LANGUAGE sql IMMUTABLE; 
 
CREATE OR REPLACE FUNCTION cast_datetime_utc(text)
RETURNS timestamp AS
$$SELECT timezone('UTC', $1::timestamptz)$$
LANGUAGE sql IMMUTABLE;
drop function cast_datetime_utc;
select cast_datetime_utc('2021-11-09 19:17:58');

SELECT timezone('UTC', '2021-11-09 19:17:58');
select now() AT TIME ZONE 'UTC';
SET TIME ZONE 'UTC';
SET TIME ZONE 'Europe/Paris';
ALTER DATABASE postgres SET timezone TO 'UTC';


SHOW time zone;
select now();

CREATE TABLE ioWatt_utc (
	siteId INT NOT NULL,
    execTime timestamp NOT NULL,
    datatime timestamp generated always as (cast_datetime_utc(data->>'date')) stored,
    label VARCHAR NOT NULL,
    apiVersion VARCHAR NOT NULL,    
    data jsonb NOT null,
    PRIMARY KEY (siteId, label, datatime)
);
CREATE UNIQUE INDEX index_iowatt_utc ON ioWatt_utc (siteId, label, datatime);
drop table ioWatt_utc;
truncate ioWatt_utc;

select exectime, datatime, label, data->>'date' as jsondate, (data->'value') from ioWatt_utc order by datatime DESC;