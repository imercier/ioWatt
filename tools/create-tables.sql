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


CREATE TABLE sunRadiation
(
    "timestamp" timestamp NOT NULL PRIMARY key unique,
    radiation numeric NOT NULL
);

CREATE TABLE pression("timestamp" timestamp NOT NULL PRIMARY key unique, pression numeric NOT NULL);
CREATE TABLE temperature("timestamp" timestamp NOT NULL PRIMARY key unique, temperature numeric NOT NULL);

select * from temperature ;