"""Gunicorn configuration file."""
bind = ":8000"
worker_class = "uvicorn.workers.UvicornWorker"
workers = 4
