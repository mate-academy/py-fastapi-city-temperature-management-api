# 🌆 Cities Temperature Management API

A FastAPI application for managing cities and tracking their temperature history using data from an external weather API.

---

## 📌 Project Description

This application provides:

* A CRUD API for managing cities
* An API to fetch and store current temperature data for all cities
* Endpoints to retrieve historical temperature data

Temperature data is fetched from an external weather service and stored in a local database.

---

## 🛠 Tech Stack

* **FastAPI**
* **SQLAlchemy (sync)**
* **SQLite**
* **Pydantic**
* **httpx (async HTTP client)**

---

## 🚀 How to Run the Application

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd py-fastapi-city-temperature-management-api
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Set environment variables

#### Windows (PowerShell):

```bash
$env:API_KEY="your_api_key"
```

#### Linux / Mac:

```bash
export API_KEY="your_api_key"
```

---

### 4. Run the application

```bash
uvicorn main:app --reload
```

---

### 5. Open API docs

```
http://127.0.0.1:8000/docs
```

---

## 📡 API Endpoints

### 🏙 Cities

| Method | Endpoint            | Description         |
| ------ | ------------------- | ------------------- |
| POST   | `/cities`           | Create a new city   |
| GET    | `/cities`           | Get all cities      |
| GET    | `/cities/{city_id}` | Get a specific city |
| PUT    | `/cities/{city_id}` | Update a city       |
| DELETE | `/cities/{city_id}` | Delete a city       |

---

### 🌡 Temperatures

| Method | Endpoint                      | Description                                        |
| ------ | ----------------------------- | -------------------------------------------------- |
| POST   | `/temperatures/update/`       | Fetch and store current temperature for all cities |
| GET    | `/temperatures/`              | Get all temperature records                        |
| GET    | `/temperatures/?city_id={id}` | Get temperatures for a specific city               |

---

## 🔄 How Temperature Update Works

1. The system retrieves all cities from the database
2. For each city, it sends an async request to the weather API
3. Extracts current temperature data
4. Stores it in the database with timestamp (UTC)

---

## 🧠 Design Decisions

* **Sync SQLAlchemy**

  * Simpler and sufficient for SQLite
  * Avoids unnecessary complexity of async DB

* **Async HTTP requests**

  * Used for external API calls to improve performance

* **Separation of concerns**

  * `models` → database
  * `schemas` → API validation/serialization
  * `crud` → business logic
  * `routers` → endpoints

* **UTC timestamps**

  * Ensures consistency across environments

---

## ⚠️ Assumptions & Simplifications

* SQLite is used instead of PostgreSQL
* No authentication/authorization
* No pagination for temperature data
* External API errors are minimally handled
* API key is provided via environment variables

---

## 🔐 Environment Variables

| Variable | Description                 |
| -------- | --------------------------- |
| API_KEY  | API key for weather service |

---

## 📁 Project Structure

```
project/
│
├── main.py
├── database.py
├── settings.py
├── dependencies.py
│
├── city/
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── router.py
│
├── temperature/
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── router.py
```

---

## ✅ Features

* Full CRUD for cities
* Temperature fetching from external API
* Historical temperature storage
* Filtering by city
* Clean architecture and separation of concerns

---

## 💡 Possible Improvements

* Add authentication (JWT)
* Add pagination
* Use PostgreSQL
* Add caching for API requests
* Improve error handling & retries
* Add tests

---

## 📬 Author

StrawHato
