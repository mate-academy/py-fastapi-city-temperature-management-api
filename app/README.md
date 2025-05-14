# City Temperature Management API

## Introduction
This project is an asyncAPI service for city temperature management written in FastAPI.

## Features
* CRUD (Create, Read, Update, Delete) API for managing city data. This is a simple API that allows you to create, read, update, and delete cities. The logic for managing cities and temperature data is split between endpoints and crud functions.
* Fetching current temperature data for all cities in the database.
* Filtering temperature data by city ID. The API stores temperature data in the database creating a history of all temperature data for each city. This allows to retrieve the history of temperature data for a specific city.

## Installing with GitHub
There is env.example file to see how to set environment variables.

  ```bash
  git clone https://github.com/dkibalenko/py-fastapi-city-temperature-management-api.git
  python3 -m venv env
  source venv/Scripts/activate
  pip install -r requirements.txt
  set OPEN_WEATHER_API_KEY
  set OPEN_WEATHER_URL
  alembic revision --autogenerate -m "Initial migration"
  alembic upgrade head
  python -m uvicorn main:app --reload
  ```

## Contributing
* Fork the repository
* Create a new branch (`git checkout -b <new_branch_name>`)
* Commit your changes (`git commit -am 'message'`)
* Push the branch to GitHub (`git push origin <new_branch_name>`)
* Create a new Pull Request