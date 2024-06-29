# City and Temperature Management API

This FastAPI application manages city data and their corresponding temperature data. It consists of two main components:

1. A CRUD (Create, Read, Update, Delete) API for managing city data.
2. An API that fetches current temperature data for all cities in the database and stores this data. Additionally, it provides endpoints to retrieve the history of temperature data.

## Features

### Part 1: City CRUD API

- **Create a new city**
  - **Endpoint:** `POST /cities`
  - **Request Body:**
    ```json
    {
      "name": "string",
      "additional_info": "string"
    }
    ```

- **Get a list of all cities**
  - **Endpoint:** `GET /cities`

- **Get details of a specific city (Optional)**
  - **Endpoint:** `GET /cities/{city_id}`

- **Update details of a specific city (Optional)**
  - **Endpoint:** `PUT /cities/{city_id}`
  - **Request Body:**
    ```json
    {
      "name": "string",
      "additional_info": "string"
    }
    ```

- **Delete a specific city**
  - **Endpoint:** `DELETE /cities/{city_id}`

### Part 2: Temperature API

- **Fetch current temperature data for all cities and store in database**
  - **Endpoint:** `POST /temperatures/update`

- **Get a list of all temperature records**
  - **Endpoint:** `GET /temperatures`

- **Get temperature records for a specific city**
  - **Endpoint:** `GET /temperatures/?city_id={city_id}`

## Models

### City Model

- **id:** Unique identifier for the city (integer)
- **name:** Name of the city (string)
- **additional_info:** Additional information about the city (string)

### Temperature Model

- **id:** Unique identifier for the temperature record (integer)
- **city_id:** Reference to the city (integer)
- **date_time:** Date and time when the temperature was recorded (datetime)
- **temperature:** Recorded temperature (float)

## Database

- Uses SQLite database.
- City and Temperature tables are created using SQLAlchemy.

## Setup

1. **Clone the repository:**
   ```
   git clone git@github.com:CharmNiovi/py-fastapi-city-temperature-management-api.git
   ```
   ```
   cd py-fastapi-city-temperature-management-api
   ```
2. **Create a virtual environment and activate it**
3. **Install the dependencies from requirements.txt**
4. **Create .env file and fill it like .env.example**
5. **Run the application:**
   ```shell
    uvicorn main:app
   ```

## Usage

    Access the API documentation at http://127.0.0.1:8000/docs or http://127.0.0.1:8000/redoc.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any changes or suggestions.


## Licensing
"The code in this project is licensed under WTFPL license."