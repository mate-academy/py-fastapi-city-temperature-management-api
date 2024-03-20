## City Temperature API

![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-brightgreen.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.28-blue.svg)
![Pydantic](https://img.shields.io/badge/Pydantic-2.6.3-brightgreen.svg)

City Temperature API is a web application built with FastAPI offering a platform
for upgrading city temperatures, and getting current weather base on city name through
external weather API.

## Features
* Fully base asynchronous API
* Using most widely used data validation library for Python - Pydantic.
* Using SQLAlchemy - designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language.
* Using Alembic as a lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python.
* Using external weather API to get current weather asynchronously base on city name.

## Installation
1. Clone git repository to your local machine:
```
    https://github.com/OlehOryshchuk/py-fastapi-city-temperature-management-api
```
2. Copy the `.env-sample` file to `.env` and configure the environment variables
    and also go https://www.weatherapi.com/my/ to get API key, and root URL
```
    cp .env-sample .env
```
3. Run command to run migration file
```
    alembic upgrade head
```
4. Run application
```
    uvicorn main:app --reload
```
