#!/usr/bin/env python
"""Package setup."""

from setuptools import (
    setup,
    find_packages,
)

install_requires = [
    'psycopg2==2.9.1',
    'requests==2.25.1',
]

dev_require = [
    'flake8==3.9.2',
    'mypy==0.910',
    'pytest-cov==2.12.1',
    'pytest-sugar==0.9.4',
    'pytest==6.2.4',
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
    extras_require={'dev': dev_require},
)
