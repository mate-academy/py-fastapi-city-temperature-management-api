# FastAPI City and Temperature Management

## Description

This FastAPI application manages city data and their corresponding temperature data.

## Features

- CRUD API for managing city data.
- API to fetch and store current temperature data for all cities in the database.
- Endpoints to retrieve temperature history.

## Endpoints

### City Endpoints

- `POST /api/cities/`: Create a new city.
- `GET /api/cities/`: Get a list of all cities.
- `DELETE /api/cities/{city_id}`: Delete a specific city.

### Temperature Endpoints

- `GET /api/temperatures/`: Get a list of all temperature records.
- `GET /api/temperatures/?city_id={city_id}`: Get temperature records for a specific city.
- `POST /api/temperatures/update`: Fetch and store current temperatures for all cities.

## Setup

1. Create a virtual environment and activate it.
2. Install the dependencies:
   ```sh
   pip install -r requirements.txt
