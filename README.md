# City and Temperature Management API

This is a FastAPI application for managing city data and their corresponding temperature data. The application allows you to create, read, update, and delete city records and to fetch and store current temperature data for all cities in the database.

## Installation

### Prerequisites

- Python 3.7+
- `virtualenv` or `venv` (optional but recommended)

### Step-by-Step Guide

1. **Clone the Repository**
    ```bash
    git clone https://github.com/Gilgumish/py-fastapi-city-temperature-management-api.git
    cd py-fastapi-city-temperature-management-api
    ```

2. **Create and Activate a Virtual Environment**

    - On macOS/Linux:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

    - On Windows:
      ```bash
      python -m venv venv
      .\venv\Scripts\activate
      ```

3. **Install the Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up the Environment Variables**
    Create a `.env` file in the project root directory and add the following content:
    ```plaintext
    WEATHER_API=http://api.weatherapi.com/v1/current.json
    WEATHER_API_KEY=YOUR_NEW_WEATHER_API_KEY
    DB_URL=sqlite+aiosqlite:///./test.db
    ```

5. **Run Database Migrations**
    ```bash
    alembic upgrade head
    ```

6. **Start the Application**
    ```bash
    uvicorn app.main:app --reload
    ```

7. **Access the Application**
    Open your web browser and go to `http://127.0.0.1:8000`.

## API Endpoints

### City CRUD API

1. **Create a New City**
    - **Endpoint**: `/cities/`
    - **Method**: `POST`

2. **Get a List of All Cities**
    - **Endpoint**: `/cities/`
    - **Method**: `GET`

3. **Get Details of a Specific City**
    - **Endpoint**: `/cities/{city_id}/`
    - **Method**: `GET`

4. **Update a Specific City**
    - **Endpoint**: `/cities/{city_id}/`
    - **Method**: `PUT`

5. **Delete a Specific City**
    - **Endpoint**: `/cities/{city_id}/`
    - **Method**: `DELETE`

### Temperature API

1. **Fetch and Store Current Temperature for All Cities**
    - **Endpoint**: `/temperatures/update`
    - **Method**: `POST`

2. **Get a List of All Temperature Records**
    - **Endpoint**: `/temperatures/`
    - **Method**: `GET`

3. **Get Temperature Records for a Specific City**
    - **Endpoint**: `/temperatures/{city_id}/`
    - **Method**: `GET`
