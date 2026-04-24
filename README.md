# FastAPI City Temperature Management API

## Overview
FastAPI‑додаток для керування містами та їхніми температурами. Реалізує CRUD‑операції для міст і температур, інтегрується з онлайн‑ресурсом погоди для отримання актуальних даних.

## Features
- Створення, перегляд і видалення міст
- Створення та перегляд температур для міст
- Оновлення температур через зовнішній API (`wttr.in`)
- Асинхронні HTTP‑запити з паралельним виконанням
- Моделі бази даних: `City` та `Temperature`

## Requirements
- Python 3.11+
- FastAPI
- SQLAlchemy
- Pydantic
- httpx
- Uvicorn

## Setup

git clone <repository-url>
cd py-fastapi-city-temperature-management-api
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

## API Endpoints
POST /cities — створити місто
GET /cities — список міст
DELETE /cities/{city_id} — видалити місто
POST /temperatures/update — отримати та зберегти температуру з API
GET /temperatures — список температур (можна фільтрувати за city_id)

## Design Notes
Таблиці названі City та Temperature згідно вимог.
Використовується httpx.AsyncClient + asyncio.gather для паралельних запитів.
.gitignore виключає локальні файли бази (cities.db).

## Assumptions
Для простоти використовується wttr.in без API‑ключа.
SQLite для локальної розробки, можна замінити на PostgreSQL/MySQL у продакшн.

## Future Improvements
Додати аутентифікацію
Реалізувати оновлення даних міст
Обробка помилок зовнішнього API
Docker‑контейнеризація
