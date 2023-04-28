FROM python:3.11.3

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.4.2

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

COPY . /app

EXPOSE 5000