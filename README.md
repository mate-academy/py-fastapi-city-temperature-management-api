# City Weather Manager API

A FastAPI application that manages a database of cities and facilitates fetching their current temperature data from an external provider (Open-Meteo).

## Project Overview

This application consists of two main components:
1.  **City CRUD API:** Endpoints to manage city data (Create, Read, Delete).
2.  **Temperature API:** An asynchronous service to fetch real-time weather data for all stored cities and maintain a history of temperature records.

## Features

* **RESTful API:** Clean endpoints for managing city and weather data.
* **Async Processing:** Uses asynchronous HTTP requests to fetch weather data without blocking the application.
* **Performance Optimized:** Implements bulk database commits to handle large updates efficiently.
* **Automatic Geocoding:** Converts city names to coordinates automatically before fetching weather data.
* **SQLite Database:** Lightweight, file-based database integration using SQLAlchemy.

---

## Setup & Installation

### Prerequisites
* Python 3.8 or higher
* pip (Python package installer)

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd weather_app
    ```

2.  **Set up a Virtual Environment:**
    * **Windows:**
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```
    * **macOS / Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install Dependencies:**
    ```bash
    pip install fastapi uvicorn sqlalchemy httpx
    ```

## Running the Application

1.  Start the local server using Uvicorn:
    ```bash
    uvicorn app.main:app --reload
    ```

2.  The API will be available at `http://127.0.0.1:8000`.

## Usage & Documentation

FastAPI provides automatic interactive documentation. Once the app is running, visit:

* **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) - Test endpoints directly from the browser.
* **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) - Alternative documentation view.

### Quick Start Workflow
1.  **Create a City:** Use `POST /cities/` to add "London".
2.  **Update Weather:** Use `POST /temperatures/update`. This triggers the background fetch.
3.  **View Data:** Use `GET /temperatures/` to see the saved record.

---

## Design Choices

* **Project Structure:** The application follows a modular structure (`routers`, `models`, `crud`, `schemas`) to separate concerns and improve maintainability.
* **Asynchronous Client (`httpx`):** The temperature update endpoint uses `httpx` instead of `requests`. This allows the application to handle multiple concurrent requests efficiently and prevents the main thread from blocking while waiting for external API responses.
* **Batch Database Commits:** The temperature update logic collects all data objects first and performs a single database commit transaction. This significantly reduces I/O overhead compared to committing records one by one inside a loop.
* **Error Handling:** The external API fetcher includes specific error handling for network issues (`httpx.RequestError`) and data parsing errors, ensuring that a failure for one city does not crash the entire batch update process.

## Assumptions & Simplifications

* **External API:** The application uses **Open-Meteo** for weather data because it is free and does not require an API key, simplifying the setup process for reviewers.
* **Geocoding:** It is assumed that the first result returned by the geocoding API is the correct city. In a production environment, a user selection step might be required to handle duplicate city names (e.g., London, UK vs. London, Ontario).
* **Database:** SQLite is used as requested. For a high-traffic production environment, this would typically be swapped for PostgreSQL.
