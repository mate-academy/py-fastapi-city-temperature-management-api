# City Temperature API

A FastAPI application that manages city data and asynchronously tracks their temperatures using Open-Meteo API.

## Requirements
- Python 3.10+
- `uv` package manager

## How to Run
1. Install dependencies and run using uv:
   ```bash
   uv run uvicorn city_temp.main:app --reload
