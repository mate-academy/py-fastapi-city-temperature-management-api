# City Temperature API

This project provides a FastAPI service that fetches the current temperature for cities stored in the database and saves them in the `Temperature` table. The service uses asynchronous requests to external APIs for geocoding and weather data.

---

## Instructions to Run

1. Clone the repository:

```bash
git clone <REPOSITORY_URL>
cd <PROJECT_FOLDER>
```

### Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### Install dependencies:

`pip install -r requirements.txt`

### Run the application:

`uvicorn app.main:app --reload`

### Test the API:

- Open Swagger UI at: http://127.0.0.1:8000/docs
- Endpoint: POST /temperatures/update/ — fetches current temperatures for all cities in the database.

## Design Choices

### Asynchronous Requests
All external API calls (geocoding and weather) are performed asynchronously using `httpx.AsyncClient`. This allows fetching data for multiple cities concurrently, improving performance and reducing wait time.

### Dependency Injection
Database sessions are injected using FastAPI's `Depends(get_db)` to keep the code clean, maintainable, and testable.

### Error Handling
- `asyncio.gather(*tasks, return_exceptions=True)` ensures that a single failing request does not stop the entire update process.
- Exceptions for individual cities are logged and skipped, allowing the remaining updates to proceed.

### Project Structure
- `services/` contains logic for external API calls (geocoding and weather).
- `city/` and `temperature/` contain models, CRUD operations, and Pydantic schemas.
- Routers are organized by resource type for clarity.

### Pydantic Schemas
Schemas validate and serialize input and output data, ensuring consistent API responses.

## Assumptions / Simplifications
- Geocoding is done using the OpenStreetMap Nominatim API.
- Weather data is fetched from the Open-Meteo API.
- Only the latest temperature per city is stored; historical records are not tracked.
- All cities are updated concurrently using asynchronous tasks.
- If a city's data fails to fetch, it is skipped without stopping the entire update process.
