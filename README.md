# POC: Palmeras UY

Django App para registro del tratamiento de las Palmeras en Montevideo

## Setup

1. `docker compose build`
1. `docker compose up`
1. `docker compose exec app uv run ./manage.py migrate`
1. `docker compose exec app uv run ./manage.py createsuperuser`
1. `docker compose exec app uv run ./manage.py load_barrios`
1. La app va a estar disponible en `http://localhost:7000`
