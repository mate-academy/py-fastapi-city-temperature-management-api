# City Temperature Tracker

This FastAPI application allows users to fetch and store temperature records for various cities. The application connects to a database to store temperature data and provides endpoints to update and retrieve these records.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Design Choices](#design-choices)
- [Assumptions and Simplifications](#assumptions-and-simplifications)

## Prerequisites

- Python 3.7 or higher
- PostgreSQL or any other supported database
- `pip` for package management

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/city-temperature-tracker.git
   cd city-temperature-tracker
   
2. Create a virtual environment (optional but recommended):
    ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the required packages:
    ```bash
   pip install -r requirements.txt
   
4. Make migrations:
    ```bash
   alembic revision --autogenerate -m "Initial migrations"
   alembic upgrade head
   
5. Create .env file with your data like data in sample.env

## Running the application

- To run the application, execute the following command:
    ```bash
    uvicorn main:app --reload
  
## API Endpoints

### Cities

- **GET /cities/**:  
  Returns all cities from the database.

- **GET /cities/{city_id}**:  
  Returns the city with the provided ID.

- **POST /cities/**:  
  Creates a new city in the database.

- **PUT /cities/{city_id}**:  
  Updates the city with the specified ID.

- **DELETE /cities/{city_id}**:  
  Deletes the city with the specified ID.

### Temperatures

- **POST /temperatures/update/**:  
  Fetches the current temperature for all cities in the database from [OpenWeatherMap](https://openweathermap.org/).

- **GET /temperatures/**:  
  Returns all temperature records from the database.

- **GET /temperatures/?city_id={city_id}**:  
  Returns the temperature records for a specific city.

## Design Choices

- **Asynchronous Programming**:  
  The application is built using asynchronous programming to handle I/O-bound tasks effectively, allowing for improved performance when fetching data from external APIs.

- **Database Interaction**:  
  SQLAlchemy's `AsyncSession` is used for database interactions, enabling non-blocking queries.

- **Error Handling**:  
  The application includes error handling for API requests and database interactions to ensure robustness and provide clear user feedback.

## Assumptions and Simplifications

- **City Data**:  
  The application assumes that city data has been pre-populated in the database.

- **Temperature API**:  
  It assumes a stable and accessible temperature API, with no fallback mechanisms implemented in case of API failures.

- **Single Database**:  
  The application is designed to work with a single database instance and does not include multi-tenant capabilities.

- **Limited Scale**:  
  It is assumed that the number of cities will be manageable, and that temperature data will not be required in real-time, simplifying the design.
