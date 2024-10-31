# FastAPI City Temperature Management

API, that allows you quickly manage cities and theirs temperatures

## Set up

### Python3 must be already installed

1. run commands:
```
git clone https://github.com/dartomOOv/py-fastapi-city-temperature-management-api.git
python -m venv venv
venv\Scripts\activate
pip install requirements.txt
```
2. run migrations:
```
alembic upgrade head
```
3. run the server:
```
uvicorn src.main:app --host 0.0.0.0 --port 8000
```
## Features

* Filtering temperature by cities id;
* Post method, that refreshes temperature for all cities created in database;
* Asynchronous code, so it executes faster.