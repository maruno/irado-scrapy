FROM python:3.10-slim as base

RUN apt-get install ca-certificates

RUN mkdir /app
WORKDIR /app
RUN pip install poetry

COPY poetry.lock /app/poetry.lock
COPY pyproject.toml /app/pyproject.toml 
COPY irado_scrapy /app/irado_scrapy

RUN poetry install

ENV PYTHONPATH=/app/
ENV SCRAPY_SETTINGS_MODULE=irado_scrapy.settings
CMD poetry run scrapy runspider irado_scrapy/spider.py
