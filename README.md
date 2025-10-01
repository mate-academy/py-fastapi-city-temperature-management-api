# 🌆 FastAPI City Temperature Management API  

A **FastAPI-based REST API** for managing cities and their temperature records.  
The project demonstrates modern Python backend practices using **FastAPI**, **SQLAlchemy (async)**, and **Pydantic v2** for data validation.  

---

## 🚀 Features  

- **City Management**  
  - Create, update, and list cities  
  - Store additional information about each city  

- **Temperature Management**  
  - Record current temperature data for all cities in db
  - Query temperatures with filtering by city_id
  - sorting support by date

- **External Weather Integration**  
  - Fetch temperature data using [WeatherAPI](https://www.weatherapi.com/)  
  - Ready to support [OpenWeatherMap](https://openweathermap.org/api) as an alternative  


- **Data Validation**  
  - Input schemas powered by Pydantic v2  
  - Conflict checks (e.g., prevent duplicate city names)  

- **Database**  
  - Async SQLAlchemy ORM  
  - Alembic migrations  
  - SQLite

---

## 🛠️ Tech Stack  

- [FastAPI](https://fastapi.tiangolo.com/) — modern, fast Python web framework  
- [SQLAlchemy (async)](https://docs.sqlalchemy.org/) — ORM with async support  
- [Alembic](https://alembic.sqlalchemy.org/) — database migrations  
- [Pydantic v2](https://docs.pydantic.dev/) — data validation  
- [Uvicorn](https://www.uvicorn.org/) — ASGI server  
- [WeatherAPI](https://www.weatherapi.com/) / [OpenWeatherMap](https://openweathermap.org/) — weather data providers  


---

## 📦 Installation  

Clone the repository:  

```bash

git clone https://github.com/Roman-Sokolov-V/py-fastapi-city-temperature-management-api.git
cd py-fastapi-city-temperature-management-api
```

Create a virtual environment and install dependencies:
```bash

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```
Apply migrations:

```bash

alembic upgrade head
```
🔑 API Keys Configuration

This project requires an API key from a weather provider. You can use either:

[WeatherAPI](https://www.weatherapi.com/) 
 (default)

[OpenWeatherMap](https://openweathermap.org/) 
 (alternative)

1. Register and get your API key

WeatherAPI: sign up and obtain a key from your dashboard

OpenWeatherMap: create an account and generate an API key

2. Environment variables

Copy the provided sample.env file and rename it to .env

Add your API keys inside .env:  
WEATHER_API_KEY=your_weatherapi_key_here (recomended)  
or  
Open_Weather_Map_API_KEY=your_openweathermap_key_here  
⚠️ Only one provider is required. The application is configured to work with WeatherAPI by default but can be easily switched to OpenWeatherMap.


▶️ Running the Project
Start the development server:
```bash

uvicorn src.main:app --reload
```

API docs available at:

Swagger UI → http://127.0.0.1:8000/docs

ReDoc → http://127.0.0.1:8000/redoc


📄 License

This project is licensed under the MIT License.