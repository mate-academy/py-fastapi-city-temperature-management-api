# FastAPI City Temperature Management API

## Introduction

This project is a FastAPI application that provides endpoints to manage cities and their temperatures. The application is divided into two main modules: `city_crud_api` and `temperature_api`.

## Installation

### Prerequisites
- Python 3.8 or higher
- `virtualenv` package (optional but recommended)

### Steps
1. **Clone the repository**

2. **Create a virtual environment (optional but recommended)**

3. **Install the dependencies**

4. **Set up the database**
    - Configure your database connection in `database.py`.

5. **Run database migrations (if using a migration tool like Alembic)**
    ```bash
    alembic upgrade head
    ```

## Running the Application

1. **Start the application**
    ```bash
    fastapi dev main.py  
    ```

2. **Access the API documentation**
    - Once the server is running, navigate to `http://127.0.0.1:8000/docs` in your browser to see the automatically generated API documentation (provided by FastAPI).

## Design Choices

- **Modular Structure**: The application is divided into two main modules (`city_crud_api` and `temperature_api`) to keep city-related and temperature-related functionalities separate. This improves code organization and maintainability.
- **SQLAlchemy ORM**: Used for database interactions to leverage the power of ORM for better database management and object-relational mapping.
- **Pydantic Schemas**: Utilized for request and response validation, ensuring data integrity and reducing boilerplate code.
- **Dependency Injection**: Managed through the `dependencies.py` file to handle common parameters and database sessions efficiently.

## Assumptions and Simplifications

- **Static API Key**: The API key for the weather service is hardcoded for simplicity. In a real-world application, it should be stored in environment variables.
- **Error Handling**: Basic error handling is implemented. For a production system, more comprehensive error handling and logging should be added.
- **Database Schema**: Assumes a simple schema for cities and temperatures. Additional fields and relationships may be required based on actual use cases.

---

Feel free to contribute or raise issues for any bugs or feature requests. Enjoy using FastAPI!