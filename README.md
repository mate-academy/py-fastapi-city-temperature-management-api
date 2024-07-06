# City Temperature Management API
This API provides endpoints to manage information about cities and their corresponding temperature records.

## Installation

### 1. Clone the repository:

```shell
git clone https://github.com/alonasorochynska/py-fastapi-city-temperature-management-api
cd py-fastapi-city-temperature-management-api
```

### 2. Create and activate virtual environment:

```shell
# for Windows
python -m venv venv
venv\Scripts\activate
# for macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies:

```shell
pip install -r requirements.txt
```


### 4. Run migrations with Alembic to set up the database schema:

```shell
alembic upgrade head
```

### 5. Configure environment variables:

```shell
WEATHER_API_URL=https://api.weatherapi.com/v1/current.json
WEATHER_API_KEY=your_weather_api_key
DB_URL=db_url_from_your_settings
```

## Usage

### 1. Run the FastAPI server:

```shell
uvicorn main:app --reload
```

### 2. Interact with the API:

* Access the Swagger UI at http://localhost:8000/docs for interactive documentation.
* Test the API endpoints using tools like Postman or cURL.

### Endpoints

* <b>GET /:</b> Root of the API.
* <b>POST /city/:</b> Create a new city.
* <b>GET /city/:</b> Retrieve a list of all cities.
* <b>GET /city/{city_id}:</b> Retrieve details of a specific city by ID.
* <b>PUT /city/{city_id}:</b> Update details of a specific city by ID.
* <b>DELETE /city/{city_id}:</b> Delete a specific city by ID.
* <b>POST /temperature/:</b> Create a new temperature record.
* <b>GET /temperature/:</b> Retrieve a list of all temperature records.
* <b>GET /temperature/{temperature_id}:</b> Retrieve details of a specific temperature record by ID.

### Technologies Used
* <b>FastAPI:</b> FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
* <b>SQLAlchemy:</b> SQLAlchemy is the Python SQL toolkit and Object-Relational Mapping (ORM) library that provides flexible and efficient SQL data access.
* <b>Alembic:</b> Alembic is a database migration tool for SQLAlchemy that provides a way to keep database schemas in sync with changes in application code.
<hr>
Feel free to expand this README with more detailed explanations, advanced usage scenarios, or any additional features of your API!