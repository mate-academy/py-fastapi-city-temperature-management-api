## City temperature management API

This project involves developing a FastAPI application to manage city data and their corresponding temperature records.
City management component allows for the creation, retrieval, updating, and deletion of city data.
Temperature management component fetches current temperature data for all cities from an online resource 
and stores this data in the database. It also provides a way to retrieve the history of temperature records 
for all cities or a specific city.

This application aims to provide an efficient and organized way to manage city information and track temperature changes over time.

# How to run

### 1. Clone repository:
```shell
git clone https://github.com/BastovOleksandr/py-fastapi-city-temperature-management-api.git
```
### 2. Create and activate 'venv' environment  
```shell
python -m venv venv
```
For Unix system
```shell
source venv/bin/activate
```
For Windows system
```shell
venv\Scripts\activate
```
### 3. Install requirements
```shell
pip install -r requirements.txt
```
### 4. Apply migrations
```shell
alembic upgrade head
```
### 5. Rename '.env.sample' file to '.env' and fill it with appropriate data (more details inside the file
### 6. Run uvicorn server
```shell
uvicorn main:app --reload
```