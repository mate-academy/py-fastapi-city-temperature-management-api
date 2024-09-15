# Temperature Update API

This FastAPI application provides an endpoint to update the current temperature for all cities in the database using data from WeatherAPI.com.

## Instructions to Run the Application

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/SuskyiVolodymyr/py-fastapi-city-temperature-management-api.git
    cd py-fastapi-city-temperature-management-api
    ```

2. **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Create .env file with your API key(example in .env.sample):**
    ```python
    WEATHER_API_KEY = 'your_weatherapi_key'
    ```

5. **Run the database migrations:**
    ```bash
    alembic upgrade head
    ```

6. **Start the FastAPI application:**
    ```bash
    uvicorn main:app --reload
    ```

### Usage
- **Endpoint to get all cities:**
    ```
    GET /cities/
    ```

- **Endpoint to get a specific city:**
    ```
    GET /cities/{city_id}
    ```

- **Endpoint to create a new city:**
    ```
    POST /cities/
    ```

- **Endpoint to update a specific city:**
    ```
    PUT /cities/{city_id}
    ```

- **Endpoint to delete a specific city:**
    ```
    DELETE /cities/{city_id}
    ```

- **Endpoint to get all temperatures:**
    ```
    GET /temperatures/
    ```

- **Endpoint to update temperatures:**
    ```
    POST /temperatures/update
    ```

## Design Choices

1. **FastAPI:** Chosen for its performance and ease of use with asynchronous programming.
2. **aiohttp:** Used for making asynchronous HTTP requests to WeatherAPI.
3. **SQLAlchemy:** Used for ORM to interact with the database.
4. **asyncio:** Utilized to manage concurrent tasks efficiently.

## Assumptions and Simplifications

1. **City Names:** Assumed that city names in the database are valid and can be used directly with WeatherAPI.
2. **Error Handling:** Basic error handling is implemented. Further improvements can be made for production use.
3. **Database:** Assumed a SQLite database, but the code can be adapted for other databases supported by SQLAlchemy.
