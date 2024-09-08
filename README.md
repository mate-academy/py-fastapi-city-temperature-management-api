# FastAPI City and Temperature Management

## Project Description

This project implements a FastAPI web application for managing city data and corresponding temperature data. The application has two main components:

1. **City CRUD API**:
   - Create, Read, Update, and Delete (CRUD) operations for managing city data.

2. **Temperature API**:
   - Fetch current temperature data for all cities in the database from an external API.
   - Store this data in the database.
   - Retrieve the history of all temperature records.

## Getting Started

### Prerequisites

Make sure you have the following installed:
- Python 3.8 or higher
- `pip` (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Irina17191/py-fastapi-city-temperature-management-api/tree/develop  
   cd py-fastapi-city-temperature-management-api  
   ```
2. Create a Virtual Environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Macos
   venv\Scripts\activate  # On Windows
   ```

3. Install the required packages:
    ```bash
   pip install -r requirements.txt
   ```
4. Create  `.env` file in the root directory of the project and add your weather API key:

   `WEATHER_API_KEY=your_weather_api_key`
   
   
## Running the Application

Start the FastAPI server using Uvicorn::
```bash
   uvicorn main:app --reload
   ```
The server will be running at http://127.0.0.1:8000. 
You can check the available endpoints using the interactive FastAPI documentation at http://127.0.0.1:8000/docs.  

## API Endpoints

City API  
- POST /cities/: Create a new city.  
- GET /cities/: Get a list of all cities.  
- GET /cities/{city_id}: Get details of a specific city.  
- PUT /cities/{city_id}: Update details of a specific city.  
- DELETE /cities/{city_id}: Delete a specific city.  

Temperature API  
- POST /temperatures/update: Fetch and store the current temperature for all cities.  
- GET /temperatures/: Get a list of all temperature records.  
- GET /temperatures/?city_id={city_id}: Get temperature records for a specific city.  


## Design Choices

FastAPI was chosen for its modern and high-performance API capabilities.  
SQLAlchemy is used for ORM and database management.  
Asynchronous code ensures high performance when making external API requests for temperature data.  


## Assumptions and Simplifications

- SQLite is used for simplicity. For a production environment, a more robust database system can be used.  
- Weather data is fetched from an open API with a public key.  

