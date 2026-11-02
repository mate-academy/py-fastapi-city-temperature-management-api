# City Temperature Management API

## Project Description

A FastAPI application for managing cities and their temperature data.

The application has two main features:

1. A CRUD (Create, Read, Update, Delete) API for managing cities.
2. An API that asynchronously fetches current temperatures for all stored cities, saves them to the database, and provides access to temperature history.

## Technologies

- Python
- FastAPI
- SQLAlchemy
- SQLite
- HTTPX
- WeatherAPI

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd py-fastapi-city-temperature-management-api
```

Install dependencies:

```bash
uv sync
```

## Configuration

1. Get a free API key from [WeatherAPI](https://www.weatherapi.com/).
2. Create a `.env` file in the project root.
3. Add your API key:

```env
WEATHER_API_KEY=your_api_key
```

## Running

Start the server:

```bash
uv run uvicorn main:app --reload
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/cities/` | Get all cities |
| POST | `/cities/` | Create a city |
| GET | `/cities/{city_id}/` | Get a city by ID |
| PUT | `/cities/{city_id}/` | Update a city |
| DELETE | `/cities/{city_id}/` | Delete a city |
| POST | `/temperatures/update/` | Fetch and save current temperatures |
| GET | `/temperatures/` | Get temperature history |
| GET | `/temperatures/?city_id=1` | Filter temperatures by city ID |

## Swagger Documentation

Interactive API documentation is available at:

http://127.0.0.1:8000/docs
