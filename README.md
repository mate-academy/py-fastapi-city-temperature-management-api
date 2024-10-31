# City Temperatures API

This project is a FastAPI application that tracks and updates temperature data for various cities using data fetched from a weather API. The application uses SQLAlchemy for database interactions and supports asynchronous operations.

## Instructions to Run the Application

### Prerequisites

- Python 3.8+
- Virtual environment (optional but recommended)
- An ASGI server (like `uvicorn`)

### Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/vladislav-tsybuliak1/py-fastapi-library-management-api.git
    ```

2. **Create and activate a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory of the project and add settings. For example:

    ```env
    WEATHER_API_KEY=your_api_key_here
    ```

5. **Run the database migrations (if any):**

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

---

Happy coding!

Soli Deo Gloria!
