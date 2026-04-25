<!-- @format -->

# Weather & City API

A complete FastAPI-based application for managing cities and their temperature measurements with async database operations and external API integration.

## Features

- **City Management (Full CRUD)** - Create, Read, Update, Delete cities with SQLite database
- **Temperature Tracking** - Fetch current temperatures from OpenWeatherMap API
- **Historical Data Storage** - Store and retrieve complete temperature history
- **Async Architecture** - Non-blocking I/O for database and API calls
- **Statistics Endpoint** - Get average, min, max temperatures per city
- **Automatic API Documentation** - Interactive Swagger UI and ReDoc
- **Dependency Injection** - Clean, testable code following FastAPI best practices

## Technology Stack

| Technology     | Purpose                                   |
| -------------- | ----------------------------------------- |
| FastAPI 0.104+ | Web framework with automatic OpenAPI docs |
| SQLAlchemy 2.0 | Async ORM for database operations         |
| aiosqlite      | Async SQLite database driver              |
| httpx          | Async HTTP client for external API calls  |
| Pydantic v2    | Data validation and serialization         |
| python-dotenv  | Environment variable management           |

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- (Optional) OpenWeatherMap API key - get free at [OpenWeatherMap](https://openweathermap.org/api)

## Complete Installation & Setup Guide

### Step 1: Create Project Directory

```bash
mkdir weather_city_api
cd weather_city_api
```
