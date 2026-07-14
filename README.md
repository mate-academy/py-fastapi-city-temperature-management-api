# City Temperature Management API

A FastAPI application designed for managing cities and tracking their temperature data.

## Features & Design Choices

* **Weather Data Provider:** The application uses **[WeatherAPI](https://weatherapi.com/)** as the external data source. This API was chosen because it allows fetching comprehensive weather information using only the city name (making it simple and highly reliable).
* **Asynchronous HTTP Client:** **`httpx`** was chosen to handle external API requests. Its native `AsyncClient` integrates seamlessly with FastAPI's asynchronous nature, preventing blocking of the main event loop during API calls.
* **Timezone Handling & SQLite Limitation:** Since SQLite does not have native support for storing and parsing timezone information (`tzinfo`) in datetime objects, the application is designed to **store timezone info separately** (or handle conversion to UTC explicitly) to maintain data consistency and ease-of-use across different databases.

---

## How to Run the Application

### 1. Install Dependencies
Make sure you have your virtual environment activated, then install the required packages:
```bash
pip install -r requirements.txt

```

### 2. Run Database Migrations

Create and apply migrations using Alembic to set up your database schema:

```bash
alembic revision --autogenerate -m "Make migrations"
alembic upgrade head

```

### 3. Start the Application

Run the FastAPI local development server using Uvicorn:

```bash
uvicorn main:app --reload

```

---

## Interactive API Documentation (Swagger UI)

Once the application is running, you can access the interactive API docs to test the endpoints directly from your browser:

* **Swagger UI:** [http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs)
