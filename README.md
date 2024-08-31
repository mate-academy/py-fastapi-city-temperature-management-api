## City temperature API

This project is a FastAPI application that manages city and temperature data. It allows you to perform CRUD operations on cities and update temperature records for those cities by fetching data from an external weather API.

## Features

- **Cities Management:**
  - Create, read, update, and delete city records.
  - Retrieve information about specific cities.

- **Temperature Records:**
  - Fetch and store temperature records for cities.
  - Update temperature data by querying an external weather API.

## Installation

To get started, clone the repository and set up a virtual environment.

```bash
git clone <repository-url>
cd <project-directory>
python -m venv venv
.venv\Scripts\activate  # On MacOS use `.venv/bin/activate`
```
Install the required dependencies:
```bash
pip install requirements.txt
```
Create and apply the database migrations:
```bash
alembic upgrade head
```

## Configuration

Create .env file in the root directory and add your configuration using .env.sample like example.

## Running the Application

To run the application, use the following command:

```bash
uvicorn main:app
```

By default, the application will be available at http://127.0.0.1:8000.

## API Endpoints

- Cities
  - GET /cities/: Retrieve a list of all cities.
  - POST /cities/: Create a new city.
  - GET /cities/{city_id}/: Retrieve details of a specific city.
  - PUT /cities/{city_id}/: Update details of a specific city.
  - DELETE /cities/{city_id}/: Delete a specific city.

- Temperatures
  - GET /temperatures/: Retrieve a list of all temperature records.
  - GET /temperatures/{city_id}/: Retrieve temperature records for a specific city.
  - POST /temperatures/update/: Fetch and update temperature data for all cities.



- The complete source code of your application.
- A README file that includes:
    - Instructions on how to run your application.
    - A brief explanation of your design choices.
    - Any assumptions or simplifications you made.

Good luck!
