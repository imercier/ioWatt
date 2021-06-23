CREATE TABLE sunEphemeride
(
    day date NOT NULL PRIMARY key unique,
    sunrise timestamp NOT NULL,
    sunset timestamp NOT NULL,
    locationName varchar(32) NOT NULL
);

select  count(*) from sunEphemeride;
select  * from sunEphemeride;
