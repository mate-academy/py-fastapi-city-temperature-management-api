# FastAPI City Temperature Management API

## Setup Instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/SashaKisliy/py-fastapi-city-temperature-management-api.git
    cd py-fastapi-city-temperature-management-api
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv\Scripts\activate
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your `.env` file with your OpenWeatherMap API key:
    ```
    API_KEY=your_api_key_here
    ```

5. Start the FastAPI application:
    ```bash
    uvicorn main:app --reload
    ```

6. The application will be available at `http://127.0.0.1:8000`.

## API Endpoints

### City CRUD API
- `POST /cities`: Create a new city.
- `GET /cities`: Get a list of all cities.
- `GET /cities/{city_id}`: Get the details of a specific city.
- `DELETE /cities/{city_id}`: Delete a specific city.

### Temperature API
- `POST /temperatures/update`: Fetch and store the current temperature for all cities.
- `GET /temperatures`: Get a list of all temperature records.
- `GET /temperatures/by_city?city_id={city_id}`: Get the temperature records for a specific city.

## Design Choices
- Used SQLite as the database for simplicity.
- Organized the project according to FastAPI project structure guidelines.
- Used dependency injection for database sessions.
- Fetching temperature data from OpenWeatherMap API.

## Assumptions and Simplifications
- Assumed the OpenWeatherMap API key is available.
- Temperature data is fetched in Celsius and converted from Kelvin.

