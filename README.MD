# City temperature API
Simple FastAPI application for managing cities data and corresponding temperatures records using outer weather API.
___

## 🔧 Technologies used and design choices:
* [X] FastAPI: quick and reliable Python framework with support of asynchronous operations.
* [X] SQAlchemy: great tool for managing ORM with asyncio support.
* [X] SQLite: widely chosen and clear in usage database. Also is possible to use PostgreSQL or other preferable relational databases. 
* [X] Pydantic: powerful instrument for handling serializing, deserializing and validation of data. 
* [X] Alembic: great and suitable tool for database migration managing.  
* [X] WeatherAPI: outer API chosen for fetching actual temperature records in real time.
___

# 💾 Setup
1. Clone this repository.
```shell
git clone https://github.com/bohdan-yatsyna/py-fastapi-city-temperature-management-api.git
cd py-fastapi-city-temperature-management-api
```
2. Create and activate a virtual environment:
🖥 Windows:
```shell
python -m venv venv
venv\Scripts\activate
```
💻 Linux/MacOS:
```shell
python -m venv venv
source venv/bin/activate
```
3. Install required packages:
```shell
pip install -r requirements.txt
```
4. Make migrations:
```shell
alembic upgrade head
```
5. Register on https://www.weatherapi.com and get API_KEY.
Create a new .env file and write it as the WEATHER_API_KEY as specified in the .sample.env file.
6. Run the server and start the application:
```
uvicorn main:app --reload
```
And open in your browser "http://127.0.0.1:8000/" 
___
## 🧾 Project structure and endpoint details

---
### City app (folder "city")
Part of the application responsible for CRUD (Create, Read, Update, Delete) API operations for managing city data.
### Temperature app (folder "temperature")
An API that fetches current temperature data from WeatherAPI for all cities in the database and stores this data, also responds for retrieving the history of all temperature data.
### Endpoints
All project endpoints are available in clear documentation. Use "http://127.0.0.1:8000/docs".
