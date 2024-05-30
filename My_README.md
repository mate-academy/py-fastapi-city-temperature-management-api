# Temperature API
Simple API on FastAPI for storing temperature in cities across the world.

## Installation
### Configue .env according to .env.sample

### Run
```bash
pip install -r requiremets.txt
uvicorn main:app
```

## Usage
#### (Visit detailed swagger documentation at /docs)
### I. Cities
* `POST /cities`: Create a new city.
* `GET /cities`: Get a list of all cities.
* `GET /cities/{city_id}`: Get the details of a specific city.
* `PUT /cities/{city_id}`: Update the details of a specific city.
* `DELETE /cities/{city_id}`: Delete a specific city.

### II. Temperatures
* `POST /temperatures/update`: Create new temperature records for all cities in the database.
* `GET /temperatures`: Get a list of all temperature records.
* `GET /temperatures/{city_id}`: Get the temperature records for a specific city.
