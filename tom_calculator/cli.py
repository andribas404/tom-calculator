"""CLI.

Contains CLI application.
CLI is invoked from entrypoint.
For the manual invoking use command `docker exec -it tom-calculator_app_1 bash`

Usage: tom-calculator [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.

Commands:
  migrate
  migrate-data

"""
import asyncio
import logging
import subprocess

import typer
from dependency_injector.wiring import Provide, inject

from tom_calculator import services
from tom_calculator.application import create_container
from tom_calculator.util import get_datadir

logger = logging.getLogger(__name__)

app = typer.Typer()


@inject
def load(
    datadir: str,
    loader_service: services.LoaderService = Provide['loader_service'],
) -> None:
    """Load data from datadir to database.

    1. Injects loader_service from container.
    2. Run service in async mode.
    """
    asyncio.run(loader_service.load(datadir))


@app.callback()
def main(ctx: typer.Context) -> None:
    """Main callback.

    1. Used to add container to the context.
    2. Invoked before every command.
    """
    container = create_container()
    ctx.obj = container


@app.command()
def migrate() -> None:
    """Command to migrate schema via alembic."""
    typer.echo('Starting migration...')
    subprocess.run(['alembic', 'upgrade', 'head'])


@app.command()
def migrate_data() -> None:
    """Command to migrate data via container's service.

    Requires TOM_DATA variable from env.
    """
    typer.echo('Migrating data...')
    datadir = str(get_datadir())
    load(datadir)


if __name__ == '__main__':  # pragma: no cover
    app()
