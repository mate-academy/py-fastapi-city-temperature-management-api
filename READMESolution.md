# City Temperature Management API


## Setup

```bash
python3 -m venv .venv
venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

## Endpoints

- `POST /cities` - create a city.
- `GET /cities` - list all cities.
- `GET /cities/{city_id}` - get a city.
- `PUT /cities/{city_id}` - update a city.
- `DELETE /cities/{city_id}` - delete a city.
- `POST /temperatures/update` - fetch current temperatures for all cities and save them.
- `GET /temperatures` - list all temperature records.
- `GET /temperatures?city_id=1` - list temperature records for one city.
