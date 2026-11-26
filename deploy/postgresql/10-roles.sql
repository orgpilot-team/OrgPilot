-- Executed once by the official PostgreSQL image on an empty development volume.
-- Passwords are injected from the local environment, never embedded in the schema.
\set ON_ERROR_STOP on
\getenv migrator_password ORGPILOT_MIGRATOR_PASSWORD
\getenv api_password ORGPILOT_API_PASSWORD
\getenv worker_password ORGPILOT_WORKER_PASSWORD

CREATE ROLE orgpilot_migrator LOGIN PASSWORD :'migrator_password' NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS;
CREATE ROLE orgpilot_api LOGIN PASSWORD :'api_password' NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS;
CREATE ROLE orgpilot_worker LOGIN PASSWORD :'worker_password' NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS;

REVOKE CONNECT, TEMPORARY ON DATABASE orgpilot FROM PUBLIC;
GRANT CONNECT ON DATABASE orgpilot TO orgpilot_migrator, orgpilot_api, orgpilot_worker;
GRANT CREATE ON DATABASE orgpilot TO orgpilot_migrator;
REVOKE ALL ON SCHEMA public FROM PUBLIC;
CREATE SCHEMA foundation AUTHORIZATION orgpilot_migrator;

-- Runtime principals get no schema/table privileges until an owning module needs them.
