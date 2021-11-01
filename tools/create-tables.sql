CREATE TABLE EnergyHistory
(
    "timestamp" timestamp NOT NULL PRIMARY key unique,
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

CREATE TABLE radiation("timestamp" timestamp NOT NULL PRIMARY key unique, radiation numeric NOT NULL);
CREATE TABLE pression("timestamp" timestamp NOT NULL PRIMARY key unique, pression numeric NOT NULL);
CREATE TABLE temperature("timestamp" timestamp NOT NULL PRIMARY key unique, temperature numeric NOT NULL);
select * from radiation order by timestamp desc;

CREATE TABLE sites
(
    id INT NOT NULL PRIMARY key unique,
    siteName varchar not null unique,
    vendorEfficient numeric not null,
    panelNumber integer not null,
    panelSurface numeric not null,
    panelRef varchar not null,
    latitude numeric not null,
    longitude numeric not null    
);
drop table sites;

select * from sites;

CREATE TABLE EnergyMetrics
(
    "timestamp" timestamp NOT NULL PRIMARY key unique,
    energyProduced numeric NOT NULL,
    isValid boolean NOT NULL
);

CREATE TABLE timeseries (
    siteId SERIAL NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    sensor VARCHAR(128) NOT NULL,
    value numeric NOT NULL
    PRIMARY KEY (siteId, sensor, timestamp)
);
drop table timeseries;
CREATE INDEX ix_timeseries_sensor ON timeseries (sensor);
CREATE INDEX ix_timeseries_timestamp ON timeseries (timestamp);
CREATE INDEX ix_timeseries_siteid ON timeseries (siteid);
truncate table timeseries;
--delete from timeseries  where "timestamp" = '2021-10-31 10:45:00';
--delete from timeseries  where siteid ='1723771';

select * from timeseries order by "timestamp" desc;
select * from timeseries where siteid ='2168697' order by "timestamp" desc;
select * from timeseries where sensor ='energy' and siteid ='1723771' order by "timestamp" desc;
