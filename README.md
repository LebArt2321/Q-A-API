# Q&A API

API на FastAPI для создания и управления вопросами и ответами (вопрос — ответ).

Проект включает:
- REST API (FastAPI)
- SQLAlchemy ORM модели для вопросов и ответов
- Alembic миграции
- Тесты на pytest с использованием FastAPI TestClient
- Dockerfile и docker-compose для запуска приложения и БД

## Структура репозитория (ключевые файлы)

- `main.py` — точка входа приложения (FastAPI). При старте применяются миграции (если запущено в контейнере/production).
- `endpoints/` — маршруты API: `questions.py`, `answers.py`.
- `db/` — конфигурация SQLAlchemy (`db.py`) и зависимость `get_db` (`dependencies.py`).
- `models/` — ORM-модели (`orm_models.py`) и Pydantic схемы (`schemas.py`).
- `migrations/` и `alembic.ini` — Alembic миграции для управления схемой базы данных.
- `tests/` — тесты и `conftest.py` для настройки тестовой БД (sqlite).
- `Dockerfile`, `docker-compose.yml` — контейнеризация и удобный запуск вместе с Postgres.

## Функциональность

- Создание/получение/удаление вопросов
- Добавление/получение/удаление ответов к вопросам

API имеет два основных роутера:
- `/questions` — операции с вопросами
- `/answers` — операции с ответами

## Требования

Список зависимостей в `requirements.txt`. Основные: Python 3.11, FastAPI, SQLAlchemy, Alembic, Uvicorn, psycopg2-binary, pytest.

## Запуск через Docker (рекомендуемый)

1) Скопируйте (или создайте) `.env`, если необходимо, и убедитесь, что в `docker-compose.yml` корректна строка подключения к БД. По умолчанию в `docker-compose.yml` используется:

```
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/postgres
```

2) Постройте и запустите сервисы:

```powershell
# В Windows PowerShell (из корня проекта)
docker-compose up --build
```

Контейнер `app` запускает `python main.py`, который в режиме запуска применит миграции Alembic (если запускается не как reloader) и запустит Uvicorn.

Приложение будет доступно по http://localhost:8000

## Локальный запуск (venv)

1) Создайте виртуальное окружение и установите зависимости:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

2) Запустите локально (если вы хотите использовать встроенный Uvicorn):

```powershell
# примените миграции перед запуском при необходимости
alembic -c alembic.ini upgrade head
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

> Примечание: `main.py` сам пытается применить миграции при старте (в контейнерном окружении), но локально удобнее запускать `alembic` вручную перед стартом.

## Миграции (Alembic)

Конфигурация Alembic — в `alembic.ini`. Для применения миграций:

```powershell
alembic -c alembic.ini upgrade head
```

Чтобы создать новую миграцию (после изменения моделей):

```powershell
alembic -c alembic.ini revision --autogenerate -m "message"
alembic -c alembic.ini upgrade head
```

## API — примеры запросов

1) Создать вопрос

```bash
curl -X POST "http://localhost:8000/questions/" -H "Content-Type: application/json" -d '{"text": "Как дела?"}'
```

2) Получить список вопросов

```bash
curl http://localhost:8000/questions/
```

3) Добавить ответ к вопросу (id = 1)

```bash
curl -X POST "http://localhost:8000/questions/1/answers/" -H "Content-Type: application/json" -d '{"user_id": "user", "text": "Хорошо!"}'
```

4) Получить ответ

```bash
curl http://localhost:8000/answers/1
```

## Тесты

Тесты используют `pytest` и FastAPI `TestClient`. Файл `tests/conftest.py` настраивает `sqlite` тестовую БД (`sqlite:///./test.db`) и делает override зависимости `get_db`.

Запуск тестов локально:

```powershell
# активируйте виртуальное окружение, затем
pytest -v
```

Тесты не требуют поднятого Postgres, так как используют sqlite-файл для изоляции.

## Отладка и распространённые проблемы

- ModuleNotFoundError: No module named 'main' — при запуске тестов внутри контейнера или в нестандартном рабочем каталоге: убедитесь, что текущая рабочая директория — корень проекта (там, где лежит `main.py`), либо добавьте корень проекта в `PYTHONPATH` перед запуском. Пример для PowerShell:

```powershell
$env:PYTHONPATH = "$PWD"; pytest -v
```

- Логи приложения записываются в `logs/app.log` (код main.py создаёт FileHandler для `/app/logs/app.log`). Убедитесь, что директория `logs` существует и доступна для записи (docker-compose монтирует `./logs` в контейнер).
