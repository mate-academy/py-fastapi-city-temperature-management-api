# City Temperature Management API

This project is a web application developed using FastAPI that allows you to manage city data and their corresponding temperature data. The application provides APIs for creating, reading, updating, and deleting city information, as well as an API for fetching current temperatures for all cities in the database.

## Project Description

### Part 1: City CRUD API

- **City Model**:
  - `id`: a unique identifier for the city.
  - `name`: the name of the city.
  - `additional_info`: any additional information about the city.

- **Endpoints**:
  - `POST /cities`: Create a new city.
  - `GET /cities`: Get a list of all cities.
  - `GET /cities/{city_id}`: (Optional) Get details of a specific city.
  - `PUT /cities/{city_id}`: (Optional) Update details of a specific city.
  - `DELETE /cities/{city_id}`: Delete a specific city.

### Part 2: Temperature API

- **Temperature Model**:
  - `id`: a unique identifier for the temperature record.
  - `city_id`: a reference to the city.
  - `date_time`: the date and time when the temperature was recorded.
  - `temperature`: the recorded temperature.

- **Endpoints**:
  - `POST /temperatures/update`: Fetch current temperatures for all cities in the database from an external resource (WeatherAPI) and store this data in the Temperature table.
  - `GET /temperatures`: Get a list of all temperature records.
  - `GET /temperatures/?city_id={city_id}`: Get temperature records for a specific city.

## Technologies Used

- **FastAPI**: A framework for building APIs with Python.
- **SQLAlchemy**: ORM for database operations (SQLite).
- **httpx**: Asynchronous HTTP client for making requests to external APIs (WeatherAPI).
- **Pydantic**: For data validation and model definition.

## Installation

To run this application, follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd city-temperature-management-api
   
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

4. Run the application:
   ```bash
   uvicorn src.main:app --port 8001
   

## Weather API Integration

For fetching the current temperature data, you can choose any weather API of your preference. In this project, I have chosen to use [WeatherAPI](https://www.weatherapi.com/). To use this API, you need to sign up on their website and obtain an `API_KEY`.

### Configuration

1. **API Key**: After signing up at WeatherAPI, generate your API key.
2. **Base URL**: The base URL for the API is also required for making requests. For WeatherAPI, it is typically `https://api.weatherapi.com/v1`.

3. **Environment Variables**: Create a `.env` file in the root of your project directory and add the following lines to it:
   ```plaintext
   API_KEY=your_api_key_here
   BASE_URL=https://api.weatherapi.com/v1
