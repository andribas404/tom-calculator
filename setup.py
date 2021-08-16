#!/usr/bin/env python
"""Package setup."""

from setuptools import (
    setup,
    find_packages,
)

install_requires = [
    'alembic==1.6.5',
    'async_exit_stack==1.0.1',
    'async_generator==1.10',
    'asyncpg==0.24.0',
    'dependency-injector==4.35.2',
    'fastapi==0.68.0',
    'psycopg2==2.9.1',
    'sqlalchemy==1.4.22',
    'uvicorn[standard]==0.13.4',
    'uvloop==0.16.0',
]

test_require = [
    'flake8==3.9.2',
    'mypy==0.910',
    'pytest-asyncio==0.15.1',
    'pytest-cov==2.12.1',
    'pytest-sugar==0.9.4',
    'pytest==6.2.4',
]

dev_require = [
    'pydevd-pycharm~=211.7142.13',
    'jupyter==1.0.0',
]

setup(
    name='tom-calculator',
    version='0.1.0',
    url="https://github.com/andribas404/tom-calculator",
    description="Tom calculator.",
    author="Andrey Petukhov",
    author_email="andribas404@gmail.com",
    packages=find_packages(include=['tom_calculator']),
    python_requires='>=3.9',
    install_requires=install_requires,
    extras_require={
        'test': test_require,
        'dev': dev_require,
    },
)
