FROM python:3.8.16-alpine3.17 as builder

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.3.2 \
    VIRTUAL_ENV=.venv \
    PATH="${PATH}:/root/.local/bin/"

# Install dev dependencies
RUN apk update \
    && apk add curl \
    && apk add --no-cache gcc libffi-dev musl-dev \
    && curl -sSL https://install.python-poetry.org | python -

WORKDIR /src
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.in-project true \
    && poetry install
COPY . .

FROM builder as final
WORKDIR /src
# RUN apk add --no-cache libffi libpq
COPY --from=builder /src/review_etl /src/.venv /src/tests ./
ENTRYPOINT [ "poetry", "run" ]
