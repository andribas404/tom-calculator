FROM python:3.9-slim-buster

COPY . /app

RUN apt-get update \
    && echo "debconf debconf/frontend select Noninteractive" | debconf-set-selections \
    # install packages
    && apt-get -qq install \
        gcc \
        libpq-dev \
        locales \
    # python setup
    && pip install --upgrade pip \
    && pip install --no-cache-dir -e /app/[dev] \
    # clean
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -qq --allow-remove-essential remove gcc \
    && apt-get -qq autoremove \
    && apt-get clean \
    && echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
    && locale-gen

COPY entrypoint.sh /

ENV PYTHONUNBUFFERED=1 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8

WORKDIR /app

ENTRYPOINT [ "/entrypoint.sh" ]
