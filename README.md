# City Temperature Management API
## Prepare the project
1. Fork the repo (GitHub repository)
1. Clone the forked repo
    ```
    git clone the-link-from-your-forked-repo
    ```
    - You can get the link by clicking the `Clone or download` button in your repo
1. Open the project folder in your IDE
1. Open a terminal in the project folder
1. Create a branch for the solution and switch on it
    ```
    git checkout -b develop
    ```
    - You can use any other name instead of `develop`
1. If you are using PyCharm - it may propose you to automatically create venv for your project 
    and install requirements in it, but if not:
    ```
    python -m venv venv
    venv\Scripts\activate (on Windows)
    source venv/bin/activate (on macOS)
    pip install -r requirements.txt
    ```
## Setup the Database: 
Ensure you have SQLite configured in your environment. The application will automatically create the database tables on startup.
## Run the Application:

````
uvicorn main:app --reload
````
The application will be available at http://127.0.0.1:8000.

##Access the API Documentation:

Swagger UI: http://127.0.0.1:8000/docs

### City Model

The `City` model is defined with the following fields:

- `id`: A unique identifier for the city.
- `name`: The name of the city.
- `additional_info`: Any additional information about the city.

### Temperature Model

The `Temperature` model is defined with the following fields:

- `id`: A unique identifier for the temperature record.
- `city_id`: A reference to the city.
- `date_time`: The date and time when the temperature was recorded.
- `temperature`: The recorded temperature.

### Endpoints
(Visit detailed swagger documentation at /docs)
I. Cities
POST /cities: Create a new city.
GET /cities: Get a list of all cities.
GET /cities/{city_id}: Get the details of a specific city.
PUT /cities/{city_id}: Update the details of a specific city.
DELETE /cities/{city_id}: Delete a specific city.
II. Temperatures
POST /temperatures/update: Create new temperature records for all cities in the database.
GET /temperatures: Get a list of all temperature records.
GET /temperatures/?city_id={city_id}: Get the temperature records for a specific city.