# City Temperature Management App

This is a FastAPI application that allows you to manage city data and temperature records. The application consists of two main components:

1. CRUD API for managing city data.
2. Temperature API for fetching and storing temperature data for cities.

### Instructions

## Installation

Clone this repository:
```
git clone https://github.com/yourusername/city-temperature-app.git
cd city-temperature-app
```

## Environment Setup

1. Rename the provided `env.sample` file to `.env` in the project directory.
2. Open the `.env` file and replace `YOUR_WEATHERAPI_KEY` with your actual
WeatherAPI API key.

## Dockerization and Running

1. Make sure you have Docker and Docker Compose installed on your system. 
You can download and install them from the official 
[Docker website](https://www.docker.com/products/docker-desktop).
2. Build and run the Docker containers using docker-compose by running 
the following command in the project directory:

```
docker-compose up --build
```

## Accessing the Application

You can now access the FastAPI application by opening your web browser 
and navigating to http://localhost:8000. You will be able to interact 
with the API using the Swagger UI provided by FastAPI by http://localhost:8000/docs/.

## Endpoints
City CRUD API
- `POST /cities`: Create a new city.
- `GET /cities`: Get a list of all cities.
- `GET /cities/{city_id}`: Get the details of a specific city.
- `PUT /cities/{city_id}`: Update the details of a specific city.
- `DELETE /cities/{city_id}`: Delete a specific city.

Temperature API
- `POST /temperatures/update`: Fetch current temperature data for all cities and store it in the database.
- `GET /temperatures`: Get a list of all temperature records.
- `GET /temperatures/?city_id={city_id}`: Get the temperature records for a specific city.

## WeatherAPI Integration

The application uses the WeatherAPI to fetch temperature data. Your API
key is read from the `.env` file automatically.

## Design Choices

- **Database**: SQLAlchemy is used as the database toolkit,
and SQLite is used as the database engine for its simplicity
and suitability for small-scale applications.

- **Asynchronous**: Asynchronous programming is utilized,
especially for the temperature API, to handle multiple 
requests concurrently without blocking the event loop.

- **Pydantic Models**: Pydantic models are used for data validation, 
serialization, and deserialization. This helps maintain a clear
structure for the API payloads.

## Assumptions and Simplifications

- **Security**: Security considerations such as authentication
and authorization are simplified for the sake of this example.
In a real-world scenario, proper security measures should be implemented.

- **Error Handling**: While error handling is considered, specific error
scenarios and responses may need to be further refined based on use cases.

- **Deployment**: This README does not cover deployment strategies
in detail. In production, you would deploy the application on
a production server, utilize environment variables for
sensitive information, and configure a production-ready database.