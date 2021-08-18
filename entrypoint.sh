#!/usr/bin/env bash
# run alembic migration on container initialization
tom-calculator migrate
# populate tables with data (only empty ones)
tom-calculator migrate-data
# run command
exec "$@";
