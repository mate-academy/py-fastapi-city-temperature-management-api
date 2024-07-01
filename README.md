# FastAPI City Temperature Management API

This project is a FastAPI-based application that handles city information
and their associated temperature data. The application is divided into two main parts:

1. A CRUD API for city data management.
2. An API to fetch and store current temperature data for all cities in the database, along with endpoints to access the historical temperature records.


### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/fastapi-city-temperature-management-api.git
   cd fastapi-city-temperature-management-api

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   For macOS
   source venv/bin/activate
   For Windows
   venv\Scripts\activate
   
3. **Install the necessary dependencies:**
   ```bash
   pip install -r requirements.txt

4. **Initialize the database:**
   ```bash
   alembic upgrade head
   
5. **Configure environment variables:**
   ```bash
   WEATHER_API_KEY=your_weather_api_key
   WEATHER_API=https://api.weatherapi.com/v1/current.json
   DB_URL=db_url_from_settings

### Running the Application

- To run the application, use the following command:
    ```bash
    uvicorn main:app --reload --log-level debug

## API Endpoints
### City API
- GET /cities: Get a list of all cities.
- GET /cities/{city_id}: Get the details of a specific city.
- POST /cities: Create a new city.
- PUT /cities/{city_id}: Update the details of a specific city.
- DELETE /cities/{city_id}: Delete a specific city.

### Temperature API

- GET /temperatures: Get a list of all temperature records.
- GET /temperatures/?city_id={city_id}: Get temperature records for a specific city.
- POST /temperatures/update: Fetch current temperature for all cities and store in the database.

### Design Choices

- **FastAPI**: Selected for its high performance and ease of use in developing APIs.
- **SQLAlchemy with AsyncSession**: Implemented for efficient asynchronous database operations.
- **Pydantic Models**: Applied for robust data validation and serialization.
- **HTTPX**: Used for making asynchronous HTTP requests to obtain temperature data.
