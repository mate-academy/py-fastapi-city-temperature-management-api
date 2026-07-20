# Installation and Running

**The project does not require environment variables.**

REST API for managing cities and their temperature records. 
Built with 
- FastAPI 
- SQLAlchemy 
- Alembic
- SQLite

### Requirements

- Python 3.12+ (или твоя версия)
- Git

### Clone repository

```bash
git clone ...
cd ...
```


## Create virtual environment

### Linux/macOS

```bash
python3 -m venv .venv
```

#### Activate

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Apply migrations

```bash
alembic upgrade head
```


## Run application

```bash
uvicorn main:app --reload
```

or

```bash
python main.py
```


## Open / Show / Use API Documentation

```
http://127.0.0.1:8000/docs
```

# Technologies

- FastAPI
- SQLAlchemy 2.0 (Async)
- Alembic
- SQLite
- Pydantic
- Uvicorn


# Project Structure

Each module contains **models, schemas, CRUD logic, and API routes**

```
project/
│
├── cities/
│   ├── crud.py
│   ├── models.py
│   ├── router.py
│   └── schemas.py
│
├── temperature/
│   ├── crud.py
│   ├── models.py
│   ├── remoteweather.py
│   ├── router.py
│   └── schemas.py
│
├── db/
├── alembic/
├── main.py
└── weather.db
```


# Cities API

|Method|Endpoint|Description|
|---|---|---|
|GET|`/cities`|Get all cities|
|GET|`/cities/{id}`|Get city by ID|
|POST|`/cities`|Create city|
|PUT|`/cities/{id}`|Update city|
|DELETE|`/cities/{id}`|Delete city|

# Temperatures API

|Method|Endpoint|Description|
|---|---|---|
|GET|`/temperatures`|Get temperatures|
|GET|`/temperatures?city_id=1`|Filter by city|
|POST|`/temperatures`|Create temperature record|
|POST|`/temperatures/update`|Update temperatures for all cities|

# Database

- One city → many temperatures
- Foreign key `temperature.city_id`

# Notes

- API documentation is available via Swagger UI.
- Database schema is managed with Alembic migrations.


