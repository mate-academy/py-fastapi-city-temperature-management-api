# City and Temperature Management API
***

This FastAPI project provides a RESTful API for managing cities and their temperature data. 
It allows you to perform CRUD (Create, Read, Update, Delete) operations on city records and fetch the current temperature for each city from an external weather API.

## Environment Variables
***

This project uses environment variables for configuration. To set up the required variables, follow these steps:

1. Create a new `.env` file in the root directory of the project.

2. Copy the contents of the `.env_sample` file into `.env`.

3. Replace the placeholder values in the `.env` file with the actual values specific to your environment.

## Installation
***

1. `pip install -r requirements.txt`
2. `alembic init alembic`
3. `alembic revision --autogenerate -m "Initial migration"`
4. `alembic upgrade head`
5. `uvicorn main:app --reload`

## Available endpoints

### City:

- `POST /cities`: Create a new city.
- `GET /cities`: Get a list of all cities.
- `GET /cities/{city_id}`: Get the details of a specific city.
- `PUT /cities/{city_id}`: Update the details of a specific city.
- `DELETE /cities/{city_id}`: Delete a specific city.

### Temperature:

- `POST /temperatures/update`: Update temperature for all cities.
- `GET /temperatures`: Get a list of all temperature records.
- `GET /temperatures/?city_id={city_id}`: Get the temperature records for a specific city.

### Documentation

`GET /docs`


## Design Choices
***

- FastAPI: FastAPI was chosen as the web framework for this project due to its asynchronous capabilities, ease of use, and automatic API documentation generation.
- Database: SQLAlchemy was used as the ORM (Object-Relational Mapping) tool to interact with the database. It allows for easy management of database models and queries.
- HTTP Client: The httpx library was used for making asynchronous HTTP requests to an external weather API to fetch temperature data for cities.
- Async/Await: Asynchronous programming was utilized for fetching temperature data and database operations to improve concurrency and responsiveness.
- API Structure: The project follows a modular structure with separate routers for city and temperature operations. This promotes code organization and maintainability.

## Assumptions and Simplifications
***

- Weather API Key: It is assumed that the API key for the external weather API is stored as an environment variable named API_KEY.
- Temperature Units: The temperature data fetched from the weather API is assumed to be in Celsius (temp_c field). No additional conversions are performed.
- City Deletion: Deletion of a city using the DELETE endpoint removes the city from the database, along with its associated temperature records.
- Error Handling: Basic error handling is implemented, including handling missing data and failed API requests. However, more comprehensive error handling and logging could be added for production use.
- Authentication and Authorization: This project does not include authentication and authorization mechanisms. In a real-world scenario, securing API endpoints would be a crucial consideration.
