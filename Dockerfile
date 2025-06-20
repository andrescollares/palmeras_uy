FROM ghcr.io/astral-sh/uv:alpine

RUN apk add --no-cache \
  fish \
  geos geos-dev \
  gdal gdal-dev\
  proj proj-dev proj-data \
  postgresql-dev \
  build-base \
  libffi-dev \
  musl-dev \
  python3-dev

ARG UID=1000 \
  GID=1000

RUN addgroup -g "$GID" appgroup && \
  adduser -D -u "$UID" -G appgroup appuser
COPY . /app
RUN chown -R appuser:appgroup /app

USER appuser

WORKDIR /app
RUN uv sync --locked

CMD ["uv", "run", "./manage.py", "runserver", "0.0.0.0:8000"]
