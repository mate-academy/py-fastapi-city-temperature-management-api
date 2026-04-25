<!-- @format -->

# Weather & City API

A FastAPI-based application for managing cities and their temperature measurements.

## Features

- **City Management (CRUD)** - Create, Read, Update, Delete cities
- **Temperature Tracking** - Fetch current temperatures from OpenWeatherMap API
- **Historical Temperature Data** - Store and retrieve temperature history
- **Async Database Operations** - Using SQLAlchemy with aiosqlite
- **Automatic API Documentation** - Swagger UI and ReDoc available

## Tech Stack

- FastAPI - Web framework
- SQLAlchemy 2.0 - Async ORM
- aiosqlite - Async SQLite driver
- httpx - Async HTTP client for API calls
- Pydantic v2 - Data validation

## Setup Instructions

### 1. Clone or create project

```bash
mkdir weather_city_api
cd weather_city_api
```
