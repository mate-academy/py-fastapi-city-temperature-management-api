# City Temperature Management API

Asynchronous REST API based on FastAPI for getting temperature records of cities.

## Features

* Create cities, update temperature records from www.weatherapi.com
* Asynchronous operations

## Technologies

* FastAPI
* SQLAlchemy
* Alembic
* Pydantic
* Uvicorn

## Installing / Getting started

### 1. Clone project from GitHub to local computer.
Open the Git Bash console in the directory where you want to place the project and run command:
```bash
git clone https://github.com/V-Shkrobatskyi/py-fastapi-city-temperature-management-api.git
```

### 2. Create and activate virtual environment

Open the project and run command:
```bash
python -m .venv venv
```

To activate virtualenv:

a) On windows:
```bash
source .venv\Scripts\activate
```

b) On macOS:
```bash
source .venv/bin/activate
```

### 3. Create a .env file

Rename `.env.sample` file to `.env`. Open it and add the all variables to it.

### 4. Run project locally

```bash
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

## API Overview

### Cities

* `POST /cities/` – Create a city
* `GET /cities/` – List cities
* `GET /cities/id/` - Retrieve a city
* `DELETE /cities/id/` - Delete a city

### Temperatures

* `POST /temperatures/update/` – Update temperatures for cities
* `GET /temperatures/` – List temperatures, filter by city id
