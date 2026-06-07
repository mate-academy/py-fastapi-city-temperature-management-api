# 🌦 Weather Management API

This is a robust **FastAPI** application designed to manage city data and track their real-time temperatures. It features an automated asynchronous system to fetch weather updates from an external API and maintains a historical record of temperature data in a database.

---

## 🛠 Tech Stack

* **Framework:** `FastAPI`
* **Database:** `SQLAlchemy` + `aiosqlite` (SQLite)
* **HTTP Client:** `httpx` (asynchronous requests)
* **Validation:** `Pydantic`

---

## 🚀 Key Features

* **🏙 City CRUD API:** Create, retrieve, and delete city records effortlessly.
* **🌡 Automated Updates:** An asynchronous batch update functionality to fetch current temperatures for all stored cities.
* **📈 Historical Data:** Keep track of temperature changes over time with persistent storage.
* **⚡ Asynchronous Design:** Fully async implementation to ensure high performance during I/O operations.

---

## 🏗 Project Structure

The project follows clean architecture principles for better maintainability:

* **`router.py`**: Handles incoming HTTP requests and response validation.
* **`crud.py`**: Business logic, database interactions, and weather service integration.
* **`models.py`**: Database table schemas (`SQLAlchemy`).
* **`schemas.py`**: Pydantic models for data serialization.



---

## 📋 API Endpoints

Once the application is running, you can explore the interactive documentation at **`http://127.0.0.1:8000/docs`**.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/cities` | Add a new city to the database |
| **GET** | `/cities` | Retrieve all cities |
| **DELETE** | `/cities/{city_id}` | Delete a city |
| **POST** | `/temperatures/update` | Update temperature data for all cities |
| **GET** | `/temperatures` | List all recorded temperatures |

---

## ⚙️ How to Run

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/pawunder1992/py-fastapi-city-temperature-management-api](https://github.com/pawunder1992/py-fastapi-city-temperature-management-api)
   cd py-fastapi-city-temperature-management-api
   
2. **Configure environment:**
**Create a .env file in the root directory:**
   ```bash
   WEATHER_API_KEY=your_actual_api_key_here

3. **Install dependencies and start the server:**
   ```bash
   pip install -r requirements.txt
   uvicorn main:app --reload