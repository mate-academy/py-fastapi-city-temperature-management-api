# City Temperature Management API

FastAPI application for managing cities and storing their temperature history.  
The project consists of two main parts:

- City CRUD API
- Temperature API that fetches current temperatures from an external service (Open-Meteo)

---

## Features

### City CRUD
- Create a city
- List all cities
- Get city details
- Update city
- Delete city

### Temperature API
- Fetch current temperature for all cities asynchronously
- Store temperature history in the database
- Retrieve all temperature records
- Filter temperature history by city

---

## Tech Stack

- FastAPI
- SQLAlchemy (ORM)
- SQLite
- Pydantic
- httpx (async HTTP client)
- Open-Meteo API

---

## Project Structure
city_temp/
├── routers/
│ ├── cities.py
│ └── temps.py
├── models.py
├── schemas.py
├── crud.py
├── utils.py
database.py
dependencies.py
settings.py
main.py


---

## How to Run

### 1. Clone repository

```bash
git clone <repo-url>
cd <repo>
```


### 2. Create virtual environment
```bash
python -m venv venv
```

Activate:

- Windows

```bash
.\venv\Scripts\activate
```

-  Mac/Linux

```bash
source venv/bin/activate
```


### 3. Install dependencies
```bash
pip install fastapi uvicorn sqlalchemy pydantic-settings httpx
```


### 4. Run the application
```bash
uvicorn main:app --reload
```

Open:
> http://127.0.0.1:8000/docs

---

## API Endpoints

### Cities
| Method | Endpoint | Description |
|-------|---------|-------------|
| POST | `/cities` | Create a new city |
| GET | `/cities` | List all cities |
| GET | `/cities/{city_id}` | Get city details |
| PUT | `/cities/{city_id}` | Update a city |
| DELETE | `/cities/{city_id}` | Delete a city |

#### Example request

```http
POST /cities

{
  "name": "Kyiv",
  "additional_info": "Ukraine"
}
```

### Temperatures
| Method | Endpoint | Description |
|-------|---------|-------------|
| POST | `/temperatures/update` | Fetch current temperatures for all cities and store history |
| GET | `/temperatures` | List all temperature records |
| GET | `/temperatures?city_id={city_id}` | Get temperature history for a specific city |


#### Example filtered request

```http
GET /temperatures?city_id=1

[
  {
    "id": 1,
    "city_id": 1,
    "date_time": "2026-02-27T18:00:00",
    "temperature": 3.7
  }
]
```

---

## Design Choices

- SQLAlchemy ORM was used for database interaction to separate business logic from API layer.
- Dependency injection is used for database sessions.
- Temperature fetching is implemented asynchronously using httpx and asyncio.gather to improve performance.
- Batch insert with a single commit is used to reduce database overhead.
- Error handling distinguishes between skipped cities (not found) and network errors.

---

## Assumptions and Simplifications

- City names are assumed to be unique. No additional uniqueness validation beyond basic constraints was implemented.
- SQLite is used as a lightweight local database instead of a production database.
- Temperature updates are triggered manually via an endpoint rather than scheduled automatically.
- No pagination was implemented for list endpoints due to the expected small dataset.
- External API responses are trusted to follow the documented schema.
- Basic console logging is used instead of a full logging system.
- Authentication and authorization were not implemented as they were outside the project scope.
