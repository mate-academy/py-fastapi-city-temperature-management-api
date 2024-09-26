## City-Temperature FastAPI 🏙️ 🌡️

There is a project where you can create your own endpoints or use existing and fetch current information from another API service!

This application has 2 main concepts:

1. A CRUD (Create, Read, Update, Delete) API for managing city data.
2. An API that fetches current temperature data for all cities in the database and stores this data in the database.


# Getting started


### Part 1: City CRUD API

1. Clone repository:
```shell
git clone https://github.com/dimak20/py-fastapi-city-temperature-management-api
```

2. Then, create and activate .venv environment  
```shell
python -m venv env
```
For Unix system
```shell
source venv/bin/activate
```

For Windows system

```shell
venv\Scripts\activate
```

3. Install requirements.txt by the command below  


```shell
pip install -r requirements.txt
```

4. You need to make migrations (project uses async sqlite darabase)
```shell
alembic upgrade head
```


### Part 2: Temperature API

In accordance with the fact that the project uses a third-party API (WeatherAPI), you need to create a .env file and add the following environment variables: WEATHER_BASE_URL and API_WEATHER_KEY.

```plaintext
Project
│
├── alembic
│   ├── versions
│   ├── env.py
|   ├──script.py.mako
│   └── README
│
├── .env (WEATHER_BASE_URL, API_WEATHER_KEY)
│   
├── alembic.ini
│   
├── database.url
│   
├── dependecies.py
│   
├── main.py
│    
├── settings.py
│   
├── README.md
│
├── city
│   ├── __init__.py
│   └── crud.py
│   ├── routers.py
│   ├── schemas.py
│   ├── models.py
│   ├── utils.py
│
└── requirements.txt
```
