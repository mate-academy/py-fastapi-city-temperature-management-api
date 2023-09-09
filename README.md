# FastAPI Weather API

This is a Python FastAPI project that provides temperature data using the api.weatherapi.com API.

## :memo: Table of Contents

- [Installation](#rocket-getting-started)
- [Design Choices](#wrench-design-choices)
- [API Endpoints](#computer-api-endpoints)

## :rocket: Installation 

1. **Clone the repository**:

   ```
   git clone https://github.com/yourusername/your-fastapi-weather-api.git
   cd your-fastapi-weather-api
   
2. **Create a virtual environment (optional but recommended):**

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`  
   
   ```

3. **Install the required dependencies:**

   ```
   pip install -r requirements.txt
   ```

4. **Set your API key as an environment variable:**
   ```
   change API_KEY in .env
   ```
5. **Run the FastAPI application:**
   ```
   uvicorn main:app --reload
   ```

## :wrench: Design Choices

### Database

```
The application uses SQLAlchemy to interact with the database.
Two tables, cities and temperatures, are defined to store city information and temperature data.
The DBCity and DBTemperature classes are used to define the table schemas,
and a relationship is established between them.
```
### FastAPI

```
FastAPI is chosen for building the RESTful API due to its performance
and automatic documentation generation using Swagger UI.
The API includes endpoints for retrieving temperature data by city name and date/time.
```

## :computer: API Endpoints

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
