FROM python:3.12.1-slim

ARG POETRY_PARAMS="--without dev"

ENV PYTHONUNBUFFERED 1
ENV PYTHONWARNINGS=ignore
ENV POETRY_VIRTUALENVS_CREATE=false

# обновление и установка рекомендованных и необходимых системных библиотек
RUN apt-get update -y --no-install-recommends
RUN apt-get install -y --no-install-recommends \
    curl `# для установки poetry` \
    git `# для установки зависимостей из git` \
    # openssl \
    gcc `# для cryptography`

# установка poetry
RUN pip install poetry

# устанавлием рабочую директорую
WORKDIR /app

# инсталляция зависимостей
COPY pyproject.toml poetry.lock /app/
RUN poetry install $POETRY_PARAMS

# копируем файлы проекта
COPY . .

CMD ["sh", "-c", "python -m alembic upgrade head && uvicorn  app.adapters.api.http.main:app --host 0.0.0.0 --port 8000"]
