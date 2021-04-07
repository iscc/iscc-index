FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

ENV ISCC_INDEX_ALLOWED_ORIGINS="*"
ENV MODULE_NAME=iscc_index.main
ENV PORT=8090
ENV LOG_LEVEL=info
ENV INDEX_ROOT=/data
ENV INDEX_COMPONENTS=true
ENV INDEX_FEATURES=true
ENV INDEX_METADATA=true

RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    pip install --upgrade pip && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false && \
    rm -rf /var/lib/apt/lists/*

COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-root --no-dev -vvv
COPY iscc_index /app/iscc_index

