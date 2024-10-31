# City Temperatures API


You are required to create a FastAPI application that manages city data and their corresponding temperature data. The application will have two main components (apps):	This project is a FastAPI application that tracks and updates temperature data for various cities using data fetched from a weather API. The application uses SQLAlchemy for database interactions and supports asynchronous operations.


1. A CRUD (Create, Read, Update, Delete) API for managing city data.	## Instructions to Run the Application
2. An API that fetches current temperature data for all cities in the database and stores this data in the database. This API should also provide a list endpoint to retrieve the history of all temperature data.	


### Part 1: City CRUD API	### Prerequisites


1. Create a new FastAPI application.	- Python 3.8+
2. Define a Pydantic model `City` with the following fields:	- Virtual environment (optional but recommended)
    - `id`: a unique identifier for the city.	- An ASGI server (like `uvicorn`)
    - `name`: the name of the city.	
    - `additional_info`: any additional information about the city.	
3. Implement a SQLite database using SQLAlchemy and create a corresponding `City` table.	
4. Implement the following endpoints:	
    - `POST /cities`: Create a new city.	
    - `GET /cities`: Get a list of all cities.	
    - **Optional**: `GET /cities/{city_id}`: Get the details of a specific city.	
    - **Optional**: `PUT /cities/{city_id}`: Update the details of a specific city.	
    - `DELETE /cities/{city_id}`: Delete a specific city.	


### Part 2: Temperature API	### Setup


1. Define a Pydantic model `Temperature` with the following fields:	1. **Clone the repository:**
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
    git clone https://github.com/pashawarganov/py-fastapi-city-temperature-management-api.git


- Use dependency injection where appropriate.	2. **Create and activate a virtual environment (optional but recommended):**
- Organize your project according to the FastAPI project structure guidelines.	


## Evaluation Criteria	    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```


Your task will be evaluated based on the following criteria:	3. **Install the required dependencies:**


- Functionality: Your application should meet all the requirements outlined above.	    ```bash
- Code Quality: Your code should be clean, readable, and well-organized.	    pip install -r requirements.txt
- Error Handling: Your application should handle potential errors gracefully.	    ```
- Documentation: Your code should be well-documented (README.md).	


## Deliverables	4. **Set up environment variables:**


Please submit the following:	    Create a `.env` file in the root directory of the project and add settings. For example:


- The complete source code of your application.	    ```env
- A README file that includes:	    WEATHER_API_KEY=your_api_key_here
    - Instructions on how to run your application.	    ```
    - A brief explanation of your design choices.	
    - Any assumptions or simplifications you made.	


Good luck!	5. **Run the database migrations (if any):**

    Make sure your database is set up and has the necessary tables. For SQLite, the tables will be created automatically by SQLAlchemy. For other databases, you might need to run migrations.

6. **Start the application:**

    Use `uvicorn` to run the FastAPI application:

    ```bash
    uvicorn main:app --reload
    ```

    The application will be available at `http://127.0.0.1:8000`.

## Design Choices

1. **Asynchronous Operations:** The application is designed to handle asynchronous operations using FastAPI and SQLAlchemy's async capabilities. This ensures non-blocking I/O operations, especially useful when fetching data from external APIs.
2. **SQLAlchemy ORM:** SQLAlchemy is used for database interactions to leverage its powerful ORM capabilities, making it easier to work with the database using Python classes and objects.
3. **Dependency Injection:** FastAPI's dependency injection system is used to manage the database session, ensuring that each request gets its own session and is properly closed after the request is processed.

## Assumptions and Simplifications

1. **Weather API:** It is assumed that the external weather API is reliable and returns data in the expected format. Error handling is in place for API failures, but the application expects a valid response structure.

2. **Database:** The example uses SQLite for simplicity, but the application is designed to support other databases by changing the `DATABASE_URL` in the environment settings.

3. **City Data:** It is assumed that the list of cities is managed within the application, and the city names are valid and match those used by the weather API.

4. **Environment Configuration:** It is assumed that environment variables are correctly set up before running the application. The `.env` file should be configured with the necessary API key.
