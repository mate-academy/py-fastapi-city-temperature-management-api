# City Temperature Management API

City Temperature Management API is a service built with FastAPI for managing temperature data of various cities.  
It supports adding, updating, deleting cities, and recording temperature measurements linked to each city. The API also allows updating temperature data by fetching from an external weather service.

---

## Features

- Add, update, and delete cities  
- Store and retrieve temperature records per city  
- Filter temperature records by city  
- Update temperature data via external weather API  
- Asynchronous interaction with SQLite database using SQLAlchemy Async ORM

---

## Installation

1. Clone the repository:  
```bash
git clone https://github.com/YBlck/py-fastapi-city-temperature-management-api.git
cd py-fastapi-city-temperature-management-api
```
2. Create and activate a virtual environment:
```bash
python -m venv .venv
```
```bash
# On Linux/macOS
source .venv/bin/activate
```

```bash
# On Windows
.venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Create .env file:
```bash
cp .env.sample .env
```
5. Run migrations to create the required tables:
```bash
alembic upgrade head
```
6. Set your API key in .env file:

```
WEATHER_API_KEY=your_api_key_here
```
For getting the key visit https://www.weatherapi.com/ and register or log in.
Go to your dashboard and copy the API key.

---

## Running the Application

Start the FastAPI server using Uvicorn:
```bash
uvicorn main:app --reload
```
By default, the API will be available at: http://127.0.0.1:8000

---

## API Documentation
Interactive API docs are automatically generated and accessible at: http://127.0.0.1:8000/docs
