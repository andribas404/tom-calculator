import asyncio
import os
import subprocess

from dependency_injector.wiring import inject, Provide
import typer

from tom_calculator import services
from tom_calculator.application import create_app

app = typer.Typer()


@inject
def load(
    datadir: str,
    loader_service: services.LoaderService = Provide['loader_service'],
):
    asyncio.run(loader_service.load(datadir))


@app.callback()
def main(
    ctx: typer.Context,
):
    main_app = create_app()
    ctx.obj = main_app


@app.command()
def migrate():
    typer.echo('Starting migration...')
    subprocess.run(['alembic', 'migrate', 'head'])


@app.command()
def migrate_data(
):
    typer.echo('Migrating data...')
    datadir = os.getenv('TOM_DATA')
    load(datadir)


if __name__ == '__main__':
    app()
