# City Temperature API

This FastAPI application manages city data and their corresponding temperature data.

## Installation

1. Clone this repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```


## Running the application

Run the following command in the project root directory:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### Cities

- `POST /cities`: Create a new city
- `GET /cities`: Get a list of all cities
- `GET /cities/{city_id}`: Get the details of a specific city
- `DELETE /cities/{city_id}`: Delete a specific city

### Temperatures

- `POST /temperatures/update`: Fetch and store current temperature for all cities
- `GET /temperatures`: Get a list of all temperature records
- `GET /temperatures/?city_id={city_id}`: Get the temperature records for a specific city

## Design Choices

- Used SQLAlchemy with SQLite for simplicity and ease of setup
- Implemented async operations for database queries and external API calls
- Separated concerns into different modules (models, schemas, CRUD operations, API routes)

## Assumptions and Simplifications

- Used a dummy URL for the weather API. In a real application, you would need to replace this with a real weather API.
- Did not implement authentication or rate limiting, which would be necessary in a production environment.
- Error handling is basic and could be improved for a production application.