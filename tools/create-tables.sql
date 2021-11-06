CREATE OR REPLACE FUNCTION cast_datetime(text)
  RETURNS timestamptz AS
$$SELECT to_timestamp($1, 'YYYY-MM-DD HH24:MI:SS')$$
  LANGUAGE sql IMMUTABLE; 
 
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

select * from iowatt order by data->>'date' DESC;
select id, exectime, data->>'date' as dateTime, data->>'inverterMode' as mode from iowatt order by id DESC;
select siteid, data->>'date' as dateTime, data->>'totalActivePower' as totalActivePower from iowatt where label = 'equipment_inverter' order by id desc;
select siteid, data->>'date' as dateTime, data->>'value' as power from iowatt where label = 'power' order by data->>'date' DESC;
select siteid,label, count(*) from iowatt group by label, siteid;
select exectime ,data->>'date' as dateTime, cast_datetime(data->>'date'), data->'value' as energy from iowatt where label = 'energy' order by data->>'date' DESC;

CREATE USER writer WITH PASSWORD 'Zo7xEru4Gg';
grant insert on iowatt to writer;
GRANT CONNECT ON DATABASE postgres TO writer;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO writer;

CREATE USER reader WITH PASSWORD 'kHhzzQmqKn';
grant select on iowatt to reader;
GRANT CONNECT ON DATABASE postgres TO reader;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO reader;
  