## FastAPI City Temperature Management Service

This FastAPI application that manages city data and their corresponding temperature data. The application consists two main components (apps):

1. A CRUD (Create, Read, Update, Delete) API for managing city data.
2. An API that fetches current temperature data for all cities in the database and stores this data in the database.


### Getting started
1. Clone the repository:
```bash
https://github.com/imelnyk007/py-fastapi-city-temperature-management-api.git
```
2. Open the folder:
```bash
cd py-fastapi-city-temperature-management-api
```
3. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate (for Windows)
source venv/bin/activate (for macOS)
```
4. Install requirements:
```bash
pip install -r requirements.txt
```
5. Register on https://www.weatherapi.com and get API_KEY.
Create a .env file and write the API_KEY as specified in the .sample.env file.

6. Make migration:
```bash
alembic upgrade head
```
7. Run service:
```bash
uvicorn main:app --reload
```

