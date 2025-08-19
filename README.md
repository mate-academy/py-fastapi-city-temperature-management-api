# City Temperature Management API

This is an asynchronous FastAPI application that allows you to manage cities and their temperatures. It integrates with an external weather API to fetch current temperature data and stores it in a SQLite/PostgreSQL database.

---


## Features

- Create, read, update, and delete cities.
- Track temperatures for each city.
- Fetch current temperature for all cities from an online weather API.
- Fully asynchronous database operations using SQLAlchemy `AsyncSession`.

---

## Installation

1. Clone the repository:

```bash
git clone <your-repo-url>
cd <your-project-folder>
```

2. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create .env with your variables:

```bash
cp .env.sample .env
```

---

## Running the Application

```bash
uvicorn main:app --reload
```
> The API will be available at http://127.0.0.1:8000.

---

## API Endpoints
### Cities

- POST /cities/ — Create a new city
- GET /cities/ — List all cities
- GET /cities/{city_id}/ — Get city details
- PUT /cities/{city_id}/ — Update a city
- DELETE /cities/{city_id}/ — Delete a city

### Temperatures

- POST /temperatures/update/ — Fetch current temperatures for all cities from WeatherAPI and store in the database.
- GET /temperatures/{city_id}/ - Get city temperature
- GET /temperatures/ - Get temperatures

---


### Design Choices

1. **Modular Project Structure**
   The project is organized as a full application with separate modules for cities (`city/`), temperatures (`temperature/`), and database management (`database/`). Each module contains its own `models`, `crud`, `schemas`, and `routes`, making the codebase easy to navigate and maintain.

2. **Asynchronous Operations**
   All database queries and external API calls are asynchronous using `AsyncSession` and `httpx.AsyncClient` to improve performance and scalability.

3. **Separate CRUD Layer**
   Business logic for interacting with the database is encapsulated in dedicated `crud` modules, keeping endpoints lean and focused on request/response handling.

4. **Optimized Data Fetching**
   Only the necessary fields (e.g., `id` and `name`) are fetched when updating temperatures, reducing memory usage and improving efficiency.

5. **WeatherAPI Integration**
   Temperature data is fetched from WeatherAPI asynchronously. Utility functions in `temperature/utils.py` handle API requests and data parsing.

6. **Clear Separation of Concerns**

   * `routes` handle HTTP endpoints.
   * `schemas` define request and response models.
   * `crud` manages database interactions.
   * `utils` provides helper functions like fetching external API data.


---
Example Usage
```bash
curl -X POST "http://127.0.0.1:8000/cities/" \
-H "Content-Type: application/json" \
-d '{"name": "London", "additional_info": "Capital of UK"}'
```
Update temperatures: 
```bash
curl -X POST "http://127.0.0.1:8000/temperatures/update/"
```

