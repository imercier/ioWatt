CREATE USER writer WITH PASSWORD 'Zo7xEru4Gg';
grant insert, update on iowatt to writer;
GRANT CONNECT ON DATABASE postgres TO writer;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO writer;

GRANT ALL PRIVILEGES on iowatt to writer;


CREATE USER reader WITH PASSWORD 'kHhzzQmqKn';
grant select on iowatt to reader;
grant select on iowatt_utc to reader;
grant select on schema public to reader;
GRANT USAGE ON SCHEMA schema_name TO username;

GRANT CONNECT ON DATABASE postgres TO reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO reader;



REVOKE TRUNCATE, REFERENCES, TRIGGER ON ALL TABLES IN SCHEMA public FROM test;
DROP USER test CASCADE;


SELECT usename AS role_name,
  CASE 
     WHEN usesuper AND usecreatedb THEN 
	   CAST('superuser, create database' AS pg_catalog.text)
     WHEN usesuper THEN 
	    CAST('superuser' AS pg_catalog.text)
     WHEN usecreatedb THEN 
	    CAST('create database' AS pg_catalog.text)
     ELSE 
	    CAST('' AS pg_catalog.text)
  END role_attributes
FROM pg_catalog.pg_user
ORDER BY role_name desc;