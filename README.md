# City and Temperature Management API

This API service allows users to manage information about cities and their corresponding temperatures. It provides endpoints for performing CRUD (Create, Read, Update, Delete) operations on cities and temperatures.

## Features

### City Management
- **Create City**: Allows users to add new cities to the database with their respective information.
- **Get All Cities**: Retrieves a list of all cities stored in the database.
- **Get City by ID**: Fetches detailed information about a specific city based on its unique identifier.
- **Get City bi name**: Fetches detailed information about a specific city based on its name.
- **Update City**: Enables users to update the information of an existing city.
- **Delete City**: Deletes a city from the database.

### Temperature Management
- **Fetch Temperature**: Retrieves the current temperature of a specified city using a third-party weather API.
- **Get All Temperatures**: Retrieves a list of all temperature records stored in the database.
- **Get Temperature by ID**: Fetches detailed information about a specific temperature record based on its unique identifier.
- **Update Temperature**: Allows users to update the temperature record of a city.
- **Delete Temperature**: Deletes a temperature record from the database.

## Technologies Used
- **FastAPI**: Python framework used for building web APIs with Python 3.7+.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **SQLite**: Lightweight relational database management system used for local development.
- **httpx**: Asynchronous HTTP client for making HTTP requests.
- **dotenv**: Python module for parsing `.env` files to load environment variables.

## Installation
1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Install dependencies using `pip install -r requirements.txt`.
4. Create a `.env` file in the root directory and add your API key for the weather service:
5. Run the application using `uvicorn main:app --reload`.

## Usage
- Use an API client such as [Postman](https://www.postman.com/) to interact with the API endpoints.
- Refer to the API documentation provided below for detailed information on each endpoint.

## API Documentation
- Visit the interactive API documentation available at `http://localhost:8000/docs` after running the application to explore and test the available endpoints.

## Contributors
- [Your Name](https://github.com/your_username)
- [Another Contributor](https://github.com/another_username)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.