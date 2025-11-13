# Q&A API — сервис вопросов и ответов

FastAPI‑приложение для управления вопросами и ответами.  
Поддерживает каскадное удаление, валидация, миграции, тесты, Docker.

---

## API — эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| `GET` | `/questions/` | Список всех вопросов |
| `POST` | `/questions/` | Создать вопрос |
| `GET` | `/questions/{id}` | Вопрос + **все ответы** |
| `DELETE` | `/questions/{id}` | Удалить вопрос (**каскадно**) |
| `POST` | `/questions/{id}/answers/` | Добавить ответ |
| `GET` | `/answers/{id}` | Получить ответ |
| `DELETE` | `/answers/{id}` | Удалить ответ |

> **Каскадное удаление**: `DELETE /questions/{id}` удаляет **все ответы**  
> **Валидация**: `text` и `user_id` — **обязательны, не пустые**  
> **Один пользователь** → **много ответов** на один вопрос

**Документация**:  
- Swagger UI: `http://localhost:8000/docs`  
- ReDoc: `http://localhost:8000/redoc`

---

## Структура проекта

```
.
├── main.py                  # запуск, миграции, логи
├── db/
│   ├── db.py                # SQLAlchemy engine, Base
│   └── dependencies.py      # get_db()
├── models/
│   ├── orm_models.py        # Question, Answer (ORM)
│   └── schemas.py           # Pydantic v2 схемы
├── endpoints/
│   ├── questions.py         # роуты вопросов
│   └── answers.py           # роуты ответов
├── tests/
│   ├── conftest.py          # тестовая SQLite БД
│   └── test_q_a.py          # юнит‑тесты
├── migrations/              # Alembic
├── logs/                    # app.log
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
└── requirements.txt
```

---

## Настройка окружения

Скопируй пример:
   ```powershell
   cp .env.example .env
   ```
---

## Запуск (Docker — **рекомендуемый**)

```powershell
git clone https://github.com/LebArt2321/Q-A-API.git
cd Q-A-API
docker-compose up --build
```

API: `http://localhost:8000`  
Swagger: `http://localhost:8000/docs`

---

## Локальный запуск

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Применить миграции
alembic -c alembic.ini upgrade head

# Запустить
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## Тесты

```powershell
# В Docker
docker-compose exec app pytest -v

# Локально
pytest -v
```

Используется изолированная SQLite (`test.db`)  
Тесты независимы — таблицы создаются/удаляются автоматически

---

## Миграции (Alembic)

Применить миграции:
```powershell
alembic -c alembic.ini upgrade head
```

Создать новую миграцию:
```powershell
alembic -c alembic.ini revision --autogenerate -m "add column"
```

---

## Примеры запросов

```bash
# Создать вопрос
curl -X POST http://localhost:8000/questions/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Как дела?"}'

# Добавить ответ
curl -X POST http://localhost:8000/questions/1/answers/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user1", "text": "Отлично!"}'

# Получить вопрос с ответами
curl http://localhost:8000/questions/1

# Удалить вопрос (удалит и все ответы)
curl -X DELETE http://localhost:8000/questions/1
```

---

## Технологии

- **FastAPI** + **Pydantic v2**
- **SQLAlchemy 2.0**
- **PostgreSQL**
- **Alembic** (миграции)
- **Docker** + **docker-compose**
- **pytest** (тесты)

---

## Логи

- **Файл**: `logs/app.log`
- **Консоль**: stdout