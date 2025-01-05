# City and Temperature Management API

This FastAPI application allows for managing city data and their corresponding temperature records. It includes functionality to create, read, update, and delete city information, as well as to fetch and store current temperature data for all cities in the database.

---

## Features

### 1. City CRUD API
- **Create, Read, Update, Delete** operations for managing city data.
- Retrieve city details and update information easily.

### 2. Temperature API
- Fetches current temperatures for all cities from an external API.
- Stores temperature data with timestamps for historical tracking.
- Provides endpoints to access temperature history for all or specific cities.

---

## Endpoints Overview

### City CRUD Endpoints
- **`POST /cities`**: Create a new city.
- **`GET /cities`**: Retrieve a list of all cities.
- **`DELETE /cities/{city_id}`**: Delete a specific city.

### Temperature Endpoints
- **`POST /temperatures/update`**: Fetch current temperatures for all cities and store them in the database.
- **`GET /temperatures`**: Retrieve all temperature records.
- **`GET /temperatures/?city_id={city_id}`**: Retrieve temperature records for a specific city.

---

## Installation

### Prerequisites
- Python 3.9 or later.
- SQLite (or another compatible database).
- `pip` for managing Python packages.

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
