# City Temperature Management API

This project implements a REST API for managing cities and storing temperature data using FastAPI and SQLAlchemy (async). It also integrates with the OpenWeatherMap API to fetch current weather for cities.

---

## Technologies

- Python 3.12+
- FastAPI
- SQLAlchemy (Async)
- SQLite (can be replaced with another DB)
- HTTPX (for async requests to OpenWeatherMap)
- Pydantic for schemas and validation
- Uvicorn as the ASGI server

---

## Installation

1. Clone the repository:

```bash
git clone <repository_url>
cd py-fastapi-city-temperature-management-api

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
.venv\Scripts\activate

3.Install dependencies:

```bash
pip install -r requirements.txt
