## Description
This FastAPI application is to manage city data and their corresponding temperature data.
It takes temperature from "https://openweathermap.org/api" and save it to database.
Also, you can get a list of all temperature records of all cities or of a specific city.
Project is written with async/await interface.

## Installing / Getting started

A quick introduction of the minimal setup you need to get app up &
running. With this You will run server with clean Database.

### Python3 must be already installed!

```shell
python3 -m venv venv 
source venv/bin/activate
pip install -r requirements.txt
touch .env
alembic upgrade head
uvicorn main:app --reload
```
Instead of "touch .env" use, please, command "echo > .env" for Windows.
Fill .env file in according to .env_sample

## Features:
- Documentation is located at: </docs/>
- CRUD for cities
- Update Temperatures for cities
- Get a list of all temperature records
- Get the temperature records for a specific city