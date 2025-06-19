# py-fastapi-city-temperature-management-api

FastAPI застосунок для керування температурою міст із використанням SQLAlchemy, Alembic та SQLite з підтримкою async/await.

## Особливості

- Async/await підтримка з SQLAlchemy 2.0 та aiosqlite
- Модульна архітектура з розділенням на `city` та `temperature` модулі
- Автоматичні міграції з Alembic
- RESTful API з повним CRUD функціоналом
- Автоматична документація з FastAPI

## Встановлення

1. Встановіть залежності:

   ```
   pip install -r requirements.txt
   ```

2. Ініціалізуйте базу даних та застосуйте міграції:

   ```
   alembic upgrade head
   ```

3. Запустіть сервер:
   ```
   uvicorn main:app --reload
   ```

## Структура проекту

```
├── main.py                 # FastAPI застосунок
├── database.py             # Налаштування async SQLAlchemy
├── dependencies.py         # FastAPI залежності
├── settings.py             # Налаштування проекту
├── temp_aquirer.py         # Заглушка для отримання температури
├── city/                   # Модуль міст
│   ├── models.py           # SQLAlchemy моделі
│   ├── schemas.py          # Pydantic схеми
│   ├── crud.py             # CRUD операції
│   └── router.py           # API endpoints
├── temperature/            # Модуль температури
│   ├── models.py           # SQLAlchemy моделі
│   ├── schemas.py          # Pydantic схеми
│   ├── crud.py             # CRUD операції
│   └── router.py           # API endpoints
├── migrations/             # Міграції Alembic
└── city_temp.db           # SQLite база даних
```

## API Endpoints

### Міста

- `POST /cities/` — створити місто
- `GET /cities/` — отримати список міст
- `GET /cities/{city_id}` — отримати місто за ID
- `PUT /cities/{city_id}` — оновити місто
- `DELETE /cities/{city_id}` — видалити місто

### Температура

- `POST /temperatures/` — додати запис температури
- `GET /temperatures/` — отримати всі записи температури
- `GET /temperatures/{temperature_id}` — отримати запис за ID
- `GET /temperatures/city/{city_id}` — отримати температуру для міста
- `GET /temperatures/city/{city_id}/latest` — остання температура для міста

## Документація API

Після запуску сервера, документація буде доступна за адресами:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Приклад використання

```python
import requests

# Створити місто
city_data = {"name": "Київ", "additional_info": "Столиця України"}
city = requests.post("http://localhost:8000/cities/", json=city_data).json()

# Додати температуру
temp_data = {"city_id": city["id"], "temperature": 25.5}
requests.post("http://localhost:8000/temperatures/", json=temp_data)

# Отримати останню температуру
latest_temp = requests.get(f"http://localhost:8000/temperatures/city/{city['id']}/latest").json()
print(f"Температура в {city['name']}: {latest_temp['temperature']}°C")
```

## Ліцензія

MIT
