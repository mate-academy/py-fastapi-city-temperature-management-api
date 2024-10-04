## Task Description

You are required to create a FastAPI application that manages city data and their corresponding temperature data. The application will have two main components (apps):

1. A CRUD (Create, Read, Update, Delete) API for managing city data.
2. An API that fetches current temperature data for all cities in the database and stores this data in the database. This API should also provide a list endpoint to retrieve the history of all temperature data.

### Part 1: City CRUD API

1. Create a new FastAPI application.
2. Define a Pydantic model `City` with the following fields:
    - `id`: a unique identifier for the city.
    - `name`: the name of the city.
    - `additional_info`: any additional information about the city.
3. Implement a SQLite database using SQLAlchemy and create a corresponding `City` table.
4. Implement the following endpoints:
    - `POST /cities`: Create a new city.
    - `GET /cities`: Get a list of all cities.
    - **Optional**: `GET /cities/{city_id}`: Get the details of a specific city.
    - **Optional**: `PUT /cities/{city_id}`: Update the details of a specific city.
    - `DELETE /cities/{city_id}`: Delete a specific city.

### Part 2: Temperature API

1. Define a Pydantic model `Temperature` with the following fields:
    - `id`: a unique identifier for the temperature record.
    - `city_id`: a reference to the city.
    - `date_time`: the date and time when the temperature was recorded.
    - `temperature`: the recorded temperature.
2. Create a corresponding `Temperature` table in the database.
3. Implement an endpoint `POST /temperatures/update` that fetches the current temperature for all cities in the database from an online resource of your choice. Store this data in the `Temperature` table. You should use an async function to fetch the temperature data.
4. Implement the following endpoints:
    - `GET /temperatures`: Get a list of all temperature records.
    - `GET /temperatures/?city_id={city_id}`: Get the temperature records for a specific city.

### Additional Requirements

- Use dependency injection where appropriate.
- Organize your project according to the FastAPI project structure guidelines.

## Evaluation Criteria

Your task will be evaluated based on the following criteria:

- Functionality: Your application should meet all the requirements outlined above.
- Code Quality: Your code should be clean, readable, and well-organized.
- Error Handling: Your application should handle potential errors gracefully.
- Documentation: Your code should be well-documented (README.md).

## Deliverables

Please submit the following:

- The complete source code of your application.
- A README file that includes:
    - Instructions on how to run your application.
    - A brief explanation of your design choices.
    - Any assumptions or simplifications you made.

Good luck!


## Deliverables work

Instructions for running your application

pip install -r requirements.txt
uvicorn app.main:app --reload

Access API: Open your browser and navigate to: http://127.0.0.1:8000/docs to access the automatically generated Swagger UI documentation

## Brief explanation of the design

FastAPI: Was chosen for the development of this application as it is a modern web framework that supports asynchronous operations and provides easy data validation through Pydantic.

SQLAlchemy: Used for working with the database, as it is one of the most popular ORM frameworks for Python, providing convenient work with databases through Python objects.

Pydantic: Used for data validation and serialization, as it integrates easily with FastAPI and supports strong data typing.

SQLite: Used as a database, as it is a built-in solution that does not require complex configuration and is ideal for small projects.

## Assumptions or simplifications

Simplify the data structure: The city model uses a simple structure with minimal fields (name and additional_info). For a full-featured application, more fields could be added, such as country, region, etc.


Temperature data: An asynchronous HTTP request is used to retrieve temperature data. In a real project, error handling and more complex logical checks would be worth implementing.


Asynchronous Database Work: Although SQLite is not ideal for high-load systems, the project uses an asynchronous driver to demonstrate working with a database.


Data Validation: Validation of input data is implemented through Pydantic models. However, more rules can be added to check the correctness of the input data.


## API

### Cities

- **POST** `/cities/` - Create a new city
- **GET** `/cities/` - Get a list of cities
- **PUT** `/cities/{city_id}` - Update city information
- **DELETE** `/cities/{city_id}` - Delete city

### Temperatures

- **POST** `/temperatures/` - Create a new temperature record
- **GET** `/temperatures/{city_id}` - Get all temperature records for a specific city
