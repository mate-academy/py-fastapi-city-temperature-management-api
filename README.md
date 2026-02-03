# How to Run

## Install dependencies:

- pip install fastapi uvicorn sqlalchemy httpx

- Start the server:

- uvicorn app.main:app --reload

## Open API docs:

http://127.0.0.1:8000/docs

### Design Choices

- FastAPI for clear async support and automatic docs

- SQLite + SQLAlchemy for simplicity

- Router-based structure for clean separation of concerns

- Dependency Injection for DB sessions


### Assumptions & Simplifications

- Temperature API uses a public endpoint without geocoding (simplified)

- No authentication included

- City names assumed unique