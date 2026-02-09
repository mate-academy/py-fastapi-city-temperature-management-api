# 🌍 City and Temperature API

FastAPI application for managing cities and storing their temperature history.

The project consists of two main parts:

1. **City CRUD API** — manage cities in the database.
2. **Temperature API** — fetch current temperature for all cities and store history.

---

## 🚀 Technologies Used

- FastAPI
- SQLAlchemy (Async)
- SQLite
- Pydantic
- httpx (async HTTP client)
- WeatherAPI (external weather service)

---

## 📦 Project Structure

The project follows a modular FastAPI structure:
- **models** → SQLAlchemy models
- **schemas** → Pydantic models
- **crud** → database logic
- **router** → API endpoints
- **service** → external API integration logic

---

## ⚙️ Setup and Run

### 1️⃣ Clone the repository

```bash
git clone https://github.com/vmyronets/py-fastapi-city-temperature-management-api.git
cd py-fastapi-city-temperature-management-api
````

### 2️⃣ Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set environment variable

Create a `.env` file in the project root:

```
WEATHER_API_KEY=your_weatherapi_key_here
```

You can get a free API key at:
[https://www.weatherapi.com/](https://www.weatherapi.com/)

### 5️⃣ Run the application

```bash
uvicorn main:app --reload
```

API documentation will be available at:

```
http://127.0.0.1:8000/docs
```

---

## 🏙 City API Endpoints

| Method | Endpoint            | Description       |
| ------ | ------------------- | ----------------- |
| POST   | `/cities`           | Create a new city |
| GET    | `/cities`           | Get all cities    |
| GET    | `/cities/{city_id}` | Get city by ID    |
| PATCH  | `/cities/{city_id}` | Update city       |
| DELETE | `/cities/{city_id}` | Delete city       |

---

## 🌡 Temperature API Endpoints

| Method | Endpoint                  | Description                                         |
| ------ | ------------------------- | --------------------------------------------------- |
| POST   | `/temperatures/update`    | Fetch and store current temperatures for all cities |
| GET    | `/temperatures`           | Get all temperature records                         |
| GET    | `/temperatures?city_id=1` | Get temperature history for a specific city         |

---

## 🧠 Design Choices

* **Async SQLAlchemy** is used for non-blocking database operations.
* **httpx.AsyncClient** is used to fetch weather data asynchronously.
* `asyncio.gather()` is used to fetch weather for multiple cities concurrently.
* Database logic is separated into `crud` modules.
* External API logic is isolated in a `service` layer.
* Dependency Injection (`Depends`) is used for database session management.
* SQLite was chosen for simplicity and educational purposes.

---

## ⚠ Assumptions & Simplifications

* SQLite is used instead of PostgreSQL for easier local setup.
* No authentication/authorization is implemented.
* Temperature update endpoint fetches only current temperature (no forecasts).
* If weather API fails for a specific city, it is skipped.

---

## 📌 Notes

* Temperatures are stored with a timestamp (`date_time`) to maintain history.
* Deleting a city automatically deletes its temperature records (cascade delete).
* DELETE endpoints return HTTP 204 (No Content).

---

## 📄 License

Educational project.
