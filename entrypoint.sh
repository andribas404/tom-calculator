#!/usr/bin/env bash
pip install -e .[dev]
tom-calculator migrate
tom-calculator migrate-data
exec "$@";
