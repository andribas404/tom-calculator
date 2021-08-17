#!/usr/bin/env bash
psql --dbname template1 --username "postgres" <<-EOSQL
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
EOSQL
