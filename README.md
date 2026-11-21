# Weather Fetcher API

## Description

Via this project, you can store cities and maintain their temperature history.

## Prerequisites

1. Create a `.env` file to store secret keys and fill it with data according to `.env.sample`.
2. To get a `WEATHER_API_KEY`, go to [WeatherAPI](https://www.weatherapi.com/), create an account, copy your API key,
   and save it in the `.env` file.

## Run

> **Note:** Docker should be installed on your machine.

```bash
docker-compose up --build
```

## Documentation

Once the application is running, interactive API documentation is available at:

- **Swagger UI:** `http://localhost:8001/docs` (or `/docs`)
- **ReDoc:** `http://localhost:8001/redoc` (or `/redoc`)

## API Endpoints

### Cities

- `POST /cities` — Create a new city
- `GET /cities` — Get a list of all cities
- `GET /cities/{city_id}` — Get details of a specific city
- `PUT /cities/{city_id}` — Update a specific city
- `DELETE /cities/{city_id}` — Delete a specific city

### Temperatures

- `POST /temperatures/update` — Fetch and save current temperatures for all cities
- `GET /temperatures` — Get a list of all temperature records (supports filtering via `?city_id={city_id}`)

## Design choices

The data from WeatherAPI is fetched via async library httpx via async client.
Func fetch_data simply makes a request for one city and return TemperatureCreate model (Schema).
To make process faster func do requests via TaskGroup and after that get result `task.result()`
and create Temperature instances in results.
Then crud.create_all_cities_temperature makes commit to bd and refresh all temperature instances and return it as a
result.

## Assumptions

To accelerate code I used async library httpx and TaskGroup with AsyncClient to make request faster (because it is I/O
bound task).
After that I get result from all tasks from TaskGroup, created Temperature instances.
add_all was used to make only 1 SQL query and refresh Temperature instances via async `db.refresh(temperature)`

## Author

Built by [Neyrony](https://github.com/Neyrony).  
Feel free to open an issue or a pull request if you have suggestions or find a bug.

