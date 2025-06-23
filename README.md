# 🌍 City Temperature API

## 📌 Description

City Temperature API is a FastAPI application designed to manage a list of cities and store historical temperature data for each city.

The application consists of:

- A full CRUD API for managing city records.
- An API for fetching and saving current temperature data for each city.
- Endpoints to retrieve historical temperature records with optional filtering.

---

## 🚀 Getting Started

### ✅ Requirements

- Python 3.8+
- pip

### 📦 Installation

1. Clone the repository or copy the project files:

```bash
git clone <your-repo-url>
cd city_temperature_api
```

2. (Optional but recommended) Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate       # On Linux/macOS
venv\Scripts\activate        # On Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Server

Start the development server using Uvicorn:

```bash
uvicorn main:app --reload
```

- Access the interactive API docs at: [http://localhost:8000/docs](http://localhost:8000/docs)
- Alternative documentation: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📐 Project Structure

```
city_temperature_api/
├── main.py           # Main FastAPI app and endpoints
├── database.py       # Database connection and session management
├── models.py         # SQLAlchemy models for City and Temperature
├── schemas.py        # Pydantic schemas for validation and response
├── crud.py           # CRUD operations for City and Temperature
├── services.py       # Async temperature fetcher (stub or real)
├── requirements.txt  # Python dependencies
├── README.md         # Documentation
```

---

## 🔌 API Endpoints

### 🌆 City Endpoints

| Method | Endpoint             | Description             |
|--------|----------------------|-------------------------|
| POST   | `/cities/`           | Create a new city       |
| GET    | `/cities/`           | List all cities         |
| GET    | `/cities/{id}`       | Get details of a city   |
| PUT    | `/cities/{id}`       | Update city information |
| DELETE | `/cities/{id}`       | Delete a city           |

### 🌡 Temperature Endpoints

| Method | Endpoint                     | Description                              |
|--------|------------------------------|------------------------------------------|
| POST   | `/temperatures/update`       | Fetch and store current temperature for all cities |
| GET    | `/temperatures/`             | List all temperature records             |
| GET    | `/temperatures/?city_id=1`   | Filter temperature records by city       |

---

## 💡 Design Decisions

- **SQLite** was chosen for simplicity and zero-configuration.
- **AIOHTTP** is used for async temperature fetching (can be replaced with real APIs like OpenWeatherMap).
- CRUD logic is separated into a `crud.py` module for maintainability.
- Pydantic models ensure validation and automatic OpenAPI documentation.

---

## 📝 Assumptions & Simplifications

- Temperature is fetched using a mocked async service (can be replaced with a real weather API).
- No authentication or user management.
- No background jobs (e.g., Celery) for periodic temperature updates — this is handled manually via endpoint.

---

## 📮 Future Improvements

- Integrate with OpenWeather or Open-Meteo API for real temperature data.
- Add authentication and rate limiting.
- Add periodic background jobs for automatic updates.
- Add unit tests and test coverage reports.

---

## 📫 Contact

For any questions or suggestions, feel free to open an issue or contact the maintainer.
