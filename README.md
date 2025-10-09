## City Temperature API

__*City Temperature API*__ - is a small project that is done to practice FastAPI, SQLAlchemy and pydentic libraries.
This project allows you to:

1. Make CRUD (Create, Read, Update, Delete) for managing city data.
2. Fetch current temperature data for all cities in the database and store those data in the database.
3. Get a cities temperature history that is storing in database

### Part 1: How to start the project?

To store current database status/migrations this project uses __alembic__ library.

1. Install dependencies:
```bash

pip install -r requirements.txt
```
2. Create the database:
```bash

alembic upgrade head
```
3. Start the project:
```bash

uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### Part 2: Cities CRUD

The __City__ model has:

1. Cities list:
```http request
GET /cities/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json

[
    {
        "id": 1,
        "name": "Berlin",
        "additional_info": "Capital of Germany"
    }
]
```
2. City detail:
```http request
GET /cities/1/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "id": 1,
  "name": "Berlin",
  "additional_info": "Capital of Germany"
}
```
3. City update:
```http request
PUT /cities/{id}/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json

Request-body:
{
  "name": "London",
  "additional_info": "Capital of UK"
}
```

### Part 3: Temperature API:

1. Temperature list:

```http request
GET /temperatures/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json

[
  {
    "date_time": "2025-10-07T11:24:38",
    "temperature": 16.88,
    "id": 1,
    "city": {
      "name": "Berlin",
      "additional_info": "Capital of Berlin",
      "id": 1
    }
  },
]
```
2. Fetch current temperatures:

```http request
POST /temperatures/update/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json

  "succeeded": [
    {
      "city": "Berlin",
      "temperature": 22.01,
      "date_time": "2025-10-07T19:19:39"
    }
  ],
  "failed": [
    {
      "city": "Landon",
      "status_code": 404
    }
  ]
}
```