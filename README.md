# City and Temperature Management API

## Overview

This project is a FastAPI application designed to manage city data and their corresponding temperature records. The application includes two main components:

1. **City CRUD API**: Manage city data (Create, Read, Update, Delete).
2. **Temperature API**: Fetch and store current temperature data for all cities and provide endpoints to retrieve temperature history.

## Features

### City CRUD API

- **POST /cities**: Create a new city.
- **GET /cities**: Get a list of all cities.
- **GET /cities/{city_id}**: (Optional) Get the details of a specific city.
- **PUT /cities/{city_id}**: (Optional) Update the details of a specific city.
- **DELETE /cities/{city_id}**: Delete a specific city.

### Temperature API

- **POST /temperatures/update**: Fetch the current temperature for all cities from an online resource and store the data.
- **GET /temperatures**: Get a list of all temperature records.
- **GET /temperatures/?city_id={city_id}**: Get the temperature records for a specific city.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/city-temperature-api.git
   cd city-temperature-api
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source env/bin/activate # On Windows, use `env\Scripts\activate`
3. Install dependencies:
   ```bash
   pip insta bll -r requirements.txt
4. Set up the database:
   ```bash
   alembic upgrade head
   
## Running the Application
1. Start the FastAPI application:
   ```bash
   uvicorn main:app --reload
2. Access the API documentation at:
   ```http://127.0.0.1:8000/docs```

## Design choices
- FastAPI: Chosen for its performance, ease of use, and automatic documentation.
- SQLAlchemy: Used for ORM to interact with the SQLite database.
- Pydantic: Used for data validation and serialization.
- Dependency Injection: Used to manage database sessions
- Project Structure:
  - app.py in the project root: Entry point for the application.
  - db directory: Contains database configurations.
  - packages directory with temperatures and cities subdirectories:
    - crud.py: Contains CRUD operations.
    - schemas.py: Defines Pydantic models.
    - router.py: Registers endpoints using APIRouter to follow best practices.

## Assumptions and Simplifications
- Temperature data is fetched from a single online resource and stored without validation for accuracy.
- Error handling is implemented to handle common scenarios such as missing city data.
- The city and temperature models are kept simple for the sake of this example.

## Contributing
1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Make your changes.
4. Commit your changes (git commit -am 'Add new feature').
5. Push to the branch (git push origin feature-branch).
6. Create a new Pull Request.

## Licence
This project is licensed under the MIT License. See the LICENSE file for details.

## Contacts
If you have any questions or suggestions, feel free to open an issue or reach out at wallian169@gmail.com

Good luck and happy coding!
