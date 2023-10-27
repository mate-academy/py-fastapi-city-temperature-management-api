# City Temperature Management API

> A FastAPI project for managing city data and their associated temperature records.

---

## 🚀 Features

- **🏙️ City Management**: CRUD operations for cities.
- **🌡️ Temperature Records**: Manage and retrieve temperature records for cities.

## 🛠️ Setup & Installation

1. **📥 Clone the Repository**

   ```bash
   git clone https://github.com/IvanGLS/py-fastapi-city-temperature-management-api
   cd py-fastapi-city-temperature-management-api
   
2. **🌐 Setup Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows -> `venv\Scripts\activate`
3. **🔗 Install Dependencies**
   ```bash
   pip install -r requirements.txt
4. **🔥 Start the Server**
   ```bash
   uvicorn main:app --reload
Navigate to http://127.0.0.1:8000 for the API.

## 📌 API Endpoints
**Cities**
- [POST] /cities/ - Create a new city.
- [GET] /cities/ - Retrieve all cities.
- [GET] /cities/{city_id} - Fetch specific city details.
- [PUT] /cities/{city_id} - Update a city.
- [DELETE] /cities/{city_id} - Remove a city.
**Temperatures**
- [POST] /temperatures/ - Log a new temperature record.
- [GET] /temperatures/ - View all temperature records.
- [GET] /temperatures/?city_id={city_id} - Fetch temperatures for a given city.
- [DELETE] /temperatures/{temperature_id} - Delete a temperature entry.
## 💽 Database
SQLite is used for lightweight data storage. The primary database file: temperature.db.

