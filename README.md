# City Temperature Management API

A FastAPI-based application designed to manage city data and track their 
current temperatures using a third-party Weather API.

## Features

* City Management: Create, list, update, and delete cities.
* Temperature Tracking: Fetch current temperatures for all stored cities from weatherapi.com.
* Pagination: Standardized paginated responses for city and temperature lists.
* Async Performance: Fully asynchronous database operations using SQLAlchemy and aiosqlite.
* Migrations: Database version control with Alembic.

## Design Choices & Assumptions
* **Failure-First Configuration:** Following best practices for production-ready 
apps, DATABASE_URL and WEATHER_API_KEY are defined as required fields in 
Pydantic. If these environment variables are missing, the application will 
raise a ValidationError on startup rather than failing silently later.

* **Database Efficiency:**
  * **Direct Object Manipulation:** To minimize redundant database queries, 
  CRUD functions (like delete_city_by_id) accept SQLAlchemy model objects 
  directly when they have already been fetched by the router for validation.
  * **Async Driver:** I utilized sqlite+aiosqlite to ensure the database 
  remains non-blocking during heavy I/O operations.
* **High-Concurrency Updates:** The `POST /temperatures/update` endpoint uses 
asyncio.TaskGroup (Python 3.11+) to fetch weather data for all cities 
simultaneously. This allows the system to scale efficiently regardless of 
how many cities are stored in the database.
* **Scalable Pagination:** All "list" endpoints utilize a centralized pagination 
dependency. This ensures consistent API responses and prevents performance 
degradation as the data grows.
* **Robust Logging:** I replaced standard print() statements with the Python 
logging module in the temperature update logic. This allows for better error 
tracking and production monitoring.
* **Modern Typing:** I leveraged the Annotated syntax for dependency injection, 
aligning with the latest FastAPI recommendations for cleaner, more readable 
code and better IDE support.

## Tech Stack

* Framework: FastAPI
* Database: SQLite (via aiosqlite)
* ORM: SQLAlchemy 2.0
* Validation: Pydantic v2
* Migrations: Alembic
* HTTP Client: HTTPX

## Installing / Getting started

**1. Clone the repository:**
```shell
  git clone https://github.com/Slava-Nykonenko/py-fastapi-city-temperature-management-api.git
  cd py-fastapi-city-temperature-management-api
```

**2. Configure Environment Variables:**

Create a .env file in the root directory, based on the .env.sample file. 
Add your Weather API key.

**3. Install Dependencies:**
```shell
  pip install -r requirements.txt
```

**4. Create and run migrations:**
```shell
  alembic revision --autogenerate -m "Initial migration"
  alembic upgrade head
```
**5. Start the server:**
```shell
  python.exe -m uvicorn main:app --reload 
```
### API Usage examples

**Cities**
* `GET /cities/`: Retrieve a paginated list of cities.
* `POST /cities/`: Register a new city.
* `DELETE /cities/{id}`: Remove a city from the database.

**Temperatures**
* `GET /temperatures/`: View stored temperature data.
* `POST /temperatures/update/`: Triggers a global update that fetches the 
latest weather data for all cities and saves it to the database.

## Links

- Repository: [GitHub](https://github.com/Slava-Nykonenko/py-fastapi-city-temperature-management-api)
- In case of sensitive bugs like security vulnerabilities, please contact
slava.nykon@gmail.com directly. We value your effort to improve the security 
and privacy of this project!
- Related projects:
  - [Emerald Railroads](https://github.com/Slava-Nykonenko/emerald-railroads)
  - [Skyway Airlines](https://github.com/Slava-Nykonenko/skyway-airlines)
  - [Statusphere](https://github.com/Slava-Nykonenko/statusphere)

## Author
Viacheslav Nykonenko<br>
[slava.nykon@gmail.com](mailto:slava.nykon@gmail.com)<br>
[GitHub](https://github.com/Slava-Nykonenko) |
[DockerHub](https://hub.docker.com/repositories/slavanykonenko) |
[LinkedIn](https://www.linkedin.com/in/viacheslav-nykonenko-49211b316/)<br>
+353 85 222 1534 <br>
Carlow, Ireland

## Licensing
The code in this project is licensed under [MIT license](LICENSE.txt).
