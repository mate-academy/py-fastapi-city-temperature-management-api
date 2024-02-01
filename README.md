# FastAPI City and Temperature Data Management Application

## How to Run the Application

### Setting Up

1. **Clone the Repository:**
   ```shell
   git clone https://github.com/olenaliuby/py-fastapi-city-temperature-management-api.git
   ```

2. **Set Up a Virtual Environment:**
   Navigate to the project directory:
   ```shell
   cd py-fastapi-city-temperature-management-api
   ```
   Create a virtual environment:
    - On Windows:
      ```shell
      python -m venv venv
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```shell
      python3 -m venv venv
      source venv/bin/activate
      ```

3. **Install Dependencies:**
   ```shell
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file based on `.env.sample` and populate it with necessary values.

   ```shell
   API_URL=https://api.openweathermap.org/data/2.5/weather
   API_KEY=Your_API_Key_Here
      ```

### Running the Server

Run the application using Uvicorn:

```shell
uvicorn main:app --reload
```

This starts the application on `localhost:8000`.

## Endpoints

### City CRUD API

- `POST /cities`: Create a new city.
- `GET /cities`: List all cities.
- `GET /cities/{city_id}`: Get details of a specific city.
- `PUT /cities/{city_id}`: Update a specific city.
- `DELETE /cities/{city_id}`: Delete a specific city.

### Temperature API

- `POST /temperatures/update`: Fetch and update temperature data for all cities.
- `GET /temperatures`: List all temperature records.
- `GET /temperatures/{city_id}`: Get temperature records for a specific city.

## Design Choices

### Application Structure

- Modular Design: Separate `city` and `temperature` modules for maintainability.
- ORM with SQLAlchemy for database interactions.

## Assumptions and Simplifications

### Assumptions

- City names are unique.
- Reliance on the accuracy of the OpenWeatherMap API for temperature data.

### Simplifications

- SQLite for simplicity in a development setup.
- No authentication and authorization implemented.
- Basic error handling, with scope for more comprehensive solutions.

## Future Enhancements

- More scalable database implementation.
- User authentication and authorization.
- Enhanced error handling and logging.
- Expanded city model with more details.
