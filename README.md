## City Temperature Management FastAPI Application

This is a FastAPI application designed to manage city data and their corresponding temperature records. The application consists of two main components:

1. City CRUD API: Manages city data including creation, retrieval, update, and deletion of city records.
2. Temperature API: Fetches current temperature data for all cities in the database and stores this data along with historical temperature records.

### Installation

1. Clone this repository to your local machine:
```
    git clone https://github.com/Altahoma/py-fastapi-city-temperature-management-api
```
2. Navigate to the project directory:
```
    cd temperature-management-app
```
3. Create a virtual environment:
```
    python -m venv venv
```
4. Activate the virtual environment:

On Windows:
```
    venv\Scripts\activate
```
On macOS and Linux:
```
    source venv/bin/activate
```
5. Install the required dependencies:
```
    pip install -r requirements.txt
```
6. Copy the `.env.sample` file to `.env` and configure the environment variables:
```
    cp .env.sample .env
```
7. Create DB and run migrations:
```
    alembic upgrade head
```

### Running the Application

1. Once the virtual environment is activated and the dependencies are installed, you can run the FastAPI application:
```
    uvicorn main:app --reload
```
2. The application will be accessible at http://127.0.0.1:8000.

### Endpoints
City CRUD API:

- `POST /cities`: Create a new city.
- `GET /cities`: Get a list of all cities.
- `GET /cities/{city_id}`: Get the details of a specific city.
- `PUT /cities/{city_id}`: Update the details of a specific city.
- `DELETE /cities/{city_id}`: Delete a specific city.

Temperature API:

- `POST /temperatures/update`: Fetches current temperature data for all cities and stores it in the database.
- `GET /temperatures`: Get a list of all temperature records.
- `GET /temperatures/?city_id={city_id}`: Get the temperature records for a specific city.

Documentation:

- `GET /docs`: To access the API documentation, you can visit the interactive Swagger UI.

### Design Choices

- The application is built using FastAPI, a modern web framework for building APIs with Python.
- SQLAlchemy is used to handle the database, and SQLite is chosen as the database engine for its simplicity.
- Pydantic models are used for data validation and serialization.
- Asynchronous programming is utilized for fetching temperature data from http://openweathermap.org.
