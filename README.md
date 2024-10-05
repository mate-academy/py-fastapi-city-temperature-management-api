# City and Temperature Management API

FastAPI project for managing city and temperature data using an external weather API.


## Installation

```
git clone https://github.com/haldaniko/py-fastapi-city-temperature-management-api.git
cd py-fastapi-city-temperature-management-api

# on macOS
python3 -m venv venv
source venv/bin/activate

# on Windows
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

(Copy .env.sample to .env and populate it with all required data.)

alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Application will be available at http://127.0.0.1:8000

## Features

* CRUD functionality for cities and temperature records.
* Automatic temperature updates from an external weather API.
* Flexible data management through RESTful endpoints.

## Demo
![demo.png](screenshots%2Fdemo.png)