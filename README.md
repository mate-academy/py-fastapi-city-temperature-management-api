# Fastapi city tempreature management

This is a simple tool for monitoring local temperatures

### This project includes several endpoints for managing:

- CRUD operations for City records
- Retrieval of all temperature records
- Updating all temperatures using data from an external API (WeatherAPI)

## Project setup
Create a virtual environment:
```shell
python -m venv venv
```

Activate the virtual environment:
On Windows:
```shell
 venv\Scripts\activate
 ```
On macOS and Linux:
```shell
source venv/bin/activate
```

Install dependencies:
```shell
pip install -r requirements.txt
```

Apply migrations:
```shell
alembic upgrade head
```

Rename .emv.template to .env file and populate it with the required data
(Generate weather api key on [weatherapi.com](https://www.weatherapi.com/). You have to register an account)

Run:
```shell
fastapi dev main.py
```

## Project documentation

Documentation is available at: 
```
http://127.0.0.1:8000/docs  
```