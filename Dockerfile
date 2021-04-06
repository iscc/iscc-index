FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
# Is based on python:3.7 which is python:3.7.x-buster -> Debian Buster

ARG POETRY_VERSION=1.1.4
ENV GUNICORN_WORKERS=1
ENV ISCC_INDEX_ALLOWED_ORIGINS="*"


RUN apt-get update && apt-get install -y --no-install-recommends openjdk-11-jre-headless \
 && pip install --upgrade pip \
 && pip install "poetry==$POETRY_VERSION" \
 && rm -rf /var/lib/apt/lists/*

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
 && poetry install --no-dev --no-ansi --no-interaction


COPY iscc_index /app/iscc_index

EXPOSE 8090

CMD exec gunicorn iscc_index.main:app -b 0.0.0.0:8090 -w ${GUNICORN_WORKERS} -k uvicorn.workers.UvicornWorker
