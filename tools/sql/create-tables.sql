CREATE OR REPLACE FUNCTION cast_datetime(text)
  RETURNS timestamptz AS
$$SELECT to_timestamp($1, 'YYYY-MM-DD HH24:MI:SS')$$
  LANGUAGE sql IMMUTABLE; 
 

 CREATE OR REPLACE FUNCTION cast_datetime_utc(text)
  RETURNS timestamp AS
$$SELECT timezone('UTC', $1::timestamptz)$$
  LANGUAGE sql IMMUTABLE;
 
 drop function cast_datetime_utc;
 
SET TIME ZONE 'Europe/Paris';
show TIME ZONE;

SELECT timezone('UTC', '2021-11-09 18:35:00');
SELECT timezone('UTC', '2021-11-09 18:35:00'::timestamptz);
select current_date, current_time;
SELECT ((timestamp '2015-10-24 18:35:00') AT TIME ZONE 'UTC');
select now() AT TIME ZONE 'UTC';

select datatime AT TIME ZONE 'UTC' as datatime, data->>'date' as jsondate from iowatt order by datatime DESC;


CREATE TABLE ioWatt (
	id BIGSERIAL primary KEY,
	siteId INT NOT NULL,
    execTime TIMESTAMP NOT NULL,
    datatime timestamp generated always as (cast_datetime(data->>'date')) stored,
    label VARCHAR NOT NULL,
    apiVersion VARCHAR NOT NULL,    
    data jsonb NOT null
);
CREATE UNIQUE INDEX index_iowatt ON ioWatt (siteId, label, datatime);


CREATE TABLE ioWatt_utc (
	id BIGSERIAL primary KEY,
	siteId INT NOT NULL,
    execTime TIMESTAMP NOT NULL,
    datatime timestamp generated always as (cast_datetime_utc(data->>'date')) stored,
    label VARCHAR NOT NULL,
    apiVersion VARCHAR NOT NULL,    
    data jsonb NOT null
);


select * from iowatt where label = 'power' order by datatime DESC;
select id, exectime, data->>'date' as dateTime, data->>'inverterMode' as mode from iowatt order by id DESC;
select siteid, data->>'date' as dateTime, data->>'totalActivePower' as totalActivePower from iowatt where label = 'equipment_inverter' order by id desc;
select siteid, data->>'date' as dateTime, data->>'value' as power from iowatt where label = 'power' order by data->>'date' DESC;
select siteid,label, count(*) from iowatt group by label, siteid;
select exectime ,data->>'date' as dateTime, cast_datetime(data->>'date'), data->'value' as energy from iowatt where label = 'energy' order by data->>'date' DESC;

select exectime ,sites.sitename, datatime, data->>'date'
from iowatt
inner join sites
on iowatt.siteid = sites.siteid
order by datatime DESC;

select siteid, label, count(*) from iowatt group by label, siteid;