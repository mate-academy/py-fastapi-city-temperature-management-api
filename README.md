# Weather API

A FastAPI application that manages cities and their temperature data by fetching information from an external weather API and storing it in a database.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration-settingspy-file)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Design Choices](#design-choices)
- [Assumptions and Simplifications](#assumptions-and-simplifications)

## Features

- **City Management**: Create, read, update, and delete city records.
- **Temperature Data**: Fetch current temperature data for cities from an external API and store it in the database.
- **Asynchronous Operations**: Utilizes asynchronous programming for improved performance.
- **Error Handling**: Comprehensive error handling to manage API and database errors gracefully.

## Installation

### Prerequisites

- **Python 3.10+**
- **pip** (Python package installer)
- **Database**: PostgreSQL or any other supported by SQLAlchemy

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/weather-api.git
   cd weather-api
   
2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   
## Configuration settings.py file

1. DATABASE_URL: Connection string for your database.
2. WEATHER_API_KEY: API key for the external weather service.
3. PROJECT_NAME: Your own project name

## Database Setup
Alembic is a lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python. It allows you to manage database schema changes over time in a consistent and easy way.

1. Create the Initial Migration
Generate the first migration script based on your current models.

   ```bash
   alembic revision --autogenerate -m "Initial migration"
This command creates a new migration file in the alembic/versions directory. Review the generated script to ensure it accurately reflects your models.

2. Apply the Migrations
   
   ```bash
   alembic upgrade head

## Running the Application
1. Start the Server
   ```bash
   uvicorn main:app --reload
The application will be accessible at http://127.0.0.1:8000.

2. API Documentation
Swagger UI: http://127.0.0.1:8000/docs

## Design Choices

1. FastAPI Framework

Chosen for its high performance, ease of use, and built-in support for asynchronous operations, which are essential for handling multiple API requests efficiently.

2. Asynchronous Programming

Utilized async and await to ensure non-blocking operations, especially when fetching data from external APIs and interacting with the database.

3. SQLAlchemy with Async Support

Leveraged SQLAlchemy's asynchronous capabilities for database interactions, providing a robust ORM layer while maintaining performance.

4. Modular Structure

Organized the project into separate modules (routers, schemas, CRUD operations) to enhance maintainability and scalability.

5. Comprehensive Error Handling

Implemented global and route-specific error handlers to manage exceptions gracefully and provide meaningful responses to clients.

## Assumptions and Simplifications

1. External Weather API

Assumed the use of weatherapi.com for fetching temperature data. The structure of the API response is expected to include temp_c and last_updated fields under the current key.

2. Database Schema

Simplified the database schema to include City and Temperature models with essential fields. Advanced features like indexing, relationships beyond city_id, and data validation are kept minimal for simplicity.

3. Error Logging

For brevity, detailed logging mechanisms are omitted. In a production environment, integrating a logging framework would be recommended.

4. Security and Authentication

The application currently does not implement authentication or authorization. It is assumed to be used in a trusted environment or will be extended with security features as needed.

5. Pagination Parameters

Assumed a simple pagination mechanism with skip and limit parameters. More sophisticated pagination or filtering can be added based on requirements.
