**City and Temperature Management API**

This FastAPI application allows you to manage cities and their temperature records. It fetches real-time temperature data from OpenWeatherMap and stores it in a SQLite database.

**Features**

City Management: Create, retrieve, and delete cities.

Temperature Management: Update temperatures for all cities using OpenWeatherMap API.

SQLite Database: Stores city and temperature data.

**Installation**

Install dependencies:

`
pip install -r requirements.txt
`

**Set up the database** 

Run migrations to create tables:

`
alembic upgrade head
`

**Start the server:**

`
uvicorn main:app --reload
`

Access the API: The API will be available at http://localhost:8000.

**API Endpoints**

POST /cities: Create a new city.

GET /cities: Get all cities.

GET /cities/{city_id}: Get a city by ID.

DELETE /cities/{city_id}: Delete a city.

**Temperature Endpoints**

GET /temperatures: Get all temperature records.

GET /temperatures/?city_id={city_id}: Get temperature records for a specific city.

POST /temperatures/update: Update temperatures for all cities from OpenWeatherMap.