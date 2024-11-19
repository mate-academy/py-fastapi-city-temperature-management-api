# FastAPI City Temperature Management API
With this tool, you can add any city to the database and retrieve temperature data for these cities,
provided the Weather API has such data available.

## Terms of Use

This project uses the Visual Crossing Corporation (“Provider”) API to fetch data.
By using this API, you agree to comply with the API Provider's
Terms of Use, which you can review at https://www.visualcrossing.com/weather-services-terms.
Please make sure to read and agree to these terms before using the application.

## Description
This project is a FastAPI application that manages city data and their corresponding temperature records. The project includes:
- A CRUD API to manage city data.
- An API to fetch current temperature data for all cities in the database, as well as historical temperature data.

## Prerequisites
- Python 3.10+

## Installation

1. Clone the repository:
   ```sh
   git clone <https://github.com/TarasFirst/py-fastapi-city-temperature-management-api.git>
   cd py-fastapi-city-temperature-management-api
   ```

2. Create a virtual environment and activate it:
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Rename the `.env_sample` file to `.env` and add your own `SECRET_KEY` value:
   ```env
   SECRET_KEY=your_secret_key_here
   ```
   You can get a free SECRET_KEY after signing up at https://www.visualcrossing.com/


## Running the Project

1. Run database migrations using Alembic:
   ```sh
   alembic upgrade head
   ```

2. Start the FastAPI server:
   ```sh
   fastapi dev app/main.py
   ```

## API Documentation

After starting the server, you can interact with the API via:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Request Examples

### Create a City
`POST /cities`
```json
{
  "name": "Kyiv",
  "additional_info": "Capital of Ukraine"
}
```

### Get All Cities
`GET /cities`

### Update a City
`PUT /cities/{city_id}`
```json
{
  "name": "Lviv",
  "additional_info": "Historical city in Ukraine"
}
```

### Delete a City
`DELETE /cities/{city_id}`


## Authors

This project was created by Taras Goncharenko.
If you have any questions, feel free to reach me at tarasgoncharenko.work@gmail.com
or through any other preferred contact method.
