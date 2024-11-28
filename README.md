# City Temperature Management API

## Description
This application provides an API for managing city data and recording temperatures. It consists of two main components:

1. CRUD operations for managing city data.
2. An API to fetch and store current temperatures for all cities in the database from an external source.

## Features
### 1. CRUD for Cities 
   1. POST /cities — Create a new city. 
   2. GET /cities — Retrieve a list of all cities. 
   3. GET /cities/{city_id} — Retrieve details about a specific city (optional). 
   4. PUT /cities/{city_id} — Update details of a specific city (optional). 
   5. DELETE /cities/{city_id} — Delete a specific city.
### 2. Temperature API 
   1. POST /temperatures/update — Fetch and store the current temperature for all cities from an external source.
   2. GET /temperatures — Retrieve a list of all temperature records.
   3. GET /temperatures/?city_id={city_id} — Retrieve the temperature history for a specific city.

# Getting Started
### 1. Clone the Repository
```
git clone <repository_url>
cd py-fastapi-city-temperature-management-api
```
### 2. Create a Virtual Environment and Install Dependencies
```
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```
### 3. Set Up the .env File

```
SECRET_KEY=your_weatherapi_key
```

### 4. Run the Application
```
uvicorn main:app --reload
```

The application will be available at: http://127.0.0.1:8000.
