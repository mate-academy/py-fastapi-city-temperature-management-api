# City temperature management

This FastAPI project is designed to handle city data and their temperature records efficiently. 
The city management module allows users to create, view, update, and remove city information. 
Meanwhile, the temperature management module fetches the latest temperature data for all cities from an online source and logs this information in the database. 
It also offers a function to retrieve the historical temperature data for all cities or a specific city.

The goal of this application is to streamline the management of city data and monitor temperature variations over time.

## Run project

### 1. Clone repository:
```shell
git clone https://github.com/Maksym-Turenko/py-fastapi-city-temperature-management-api.git
```
### 2. Create and activate '.venv' 
```shell
python -m venv .venv
```
#### Activate for Windows
```shell
.\.venv\Scripts\activate
```
#### Activate for Unix
```shell
source .venv/bin/activate
```
### 3. Install requirements
```shell
pip install -r requirements.txt
```
### 4. Apply migrations
```shell
alembic upgrade head
```
### 5. Create .env file, enter the data that is mentioned in .env.sample
### 6. Run uvicorn server
```shell
uvicorn main:app --reload
```