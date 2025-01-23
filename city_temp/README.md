# **City and Temperature Tracker**

## **Description**
A FastAPI application to manage city data and track corresponding temperature records. This project includes:
- CRUD operations for city data.
- APIs to fetch and store temperature data for cities.

---

## Setup Instructions

### Clone the Repository
Clone the repository and navigate to the project folder.
```bash
git clone https://github.com/Illya-Maznitskiy/py-fastapi-city-temperature-management-api.git
cd py-fastapi-city-temperature-management-api
```

### Install Dependencies
Ensure Python is installed and install the required dependencies by using `requirements.txt`.
```bash
pip install -r requirements.txt
```

### Set Up the Database
The application uses SQLite by default. Ensure the database is created, and any necessary migrations are applied.
```bash
alembic upgrade head
```

### Create env file and add API weather key
Create the .env file with env.sample example
Add API key with api.openweathermap.org

### Run the Application
Start the FastAPI server to run the application locally.
```bash
uvicorn main:app --reload 
```

### Access the API Documentation
Once the server is running, access the API documentation at:
- Swagger UI: `/docs`

## Key Features

### City Management:
- Create, read, update, and delete city data.

### Temperature Tracking:
- Fetch current temperatures for all cities.
- Store and retrieve temperature history.
