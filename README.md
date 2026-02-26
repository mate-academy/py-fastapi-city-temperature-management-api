## Project Description

A FastAPI application that manages city data and their corresponding temperature data. 

Followed the mentor's design (two apps): 
1. City - for managing city data.
2. Temperature - API that fetches current temperature data for all cities in the database and stores this data in the database. Also provides a list endpoint to retrieve the history of all temperature data.

#### City endpoints
1. GET /cities/ 
2. POST /cities/
3. GET /cities/{city_id}/
4. PUT /cities/{city_id}/
5. DELETE /cities/{city_id}/ 

#### Temperature endpoints
1. GET /temperatures/
2. POST /temperatures/update
3. GET /temperatures/?city_id={city_id}


### Technologies used
- FastAPI with async endpoints
- SQLAlchemy 2.0
- async_sessionmaker
- Pydantic v2
- pydantic-settings
- Alembic async migrations
- httpx for external API calls


### How to run the application
- Clone the repo 
```bash
https://github.com/Liliyakhu/py-fastapi-city-temperature-management-api 
```
- Create .venv 
```bash
python -m venv .venv
```
- Activate the .venv 
```bash
source .venv/bin/activate
```
- Install requirements 
```bash
pip install -r requirements.txt
```
- Create .env file with 
```bash 
WEATHER_API_KEY=your_api_key_here
DATABASE_URL=sqlite+aiosqlite:///./city_temperature_db.db
```
- Run migrations
```bash
alembic upgrade head
```
- Start the server 
```bash
uvicorn main:app --reload
```
- Open http://127.0.0.1:8000/docs to test the endpoints
