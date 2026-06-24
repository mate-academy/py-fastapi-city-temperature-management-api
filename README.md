# City Temperature Management API

A comprehensive **FastAPI** application designed to manage global city metadata (via a full CRUD API) and automatically synchronize real-time temperature data from external web resources using concurrent asynchronous operations.


# Project Structure

The project strictly follows the official FastAPI project structure guidelines, separating database management, business logic layers, and route components:

py-fastapi-city-temperature-management-api/
│
├── app/
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── cities.py          # CRUD API endpoints for managing city data
│   │   └── temperatures.py    # Endpoints for syncing and retrieving temperature history
│   │
│   ├── __init__.py
│   ├── crud.py                # Database interaction layer utilizing SQLAlchemy 2.0
│   ├── database.py            # SQLite database engine connection and session setups
│   ├── models.py              # Relational database ORM models
│   ├── schemas.py             # Pydantic v2 data validation and serialization models
│   └── services.py            # Async network service layer for external API integrations
│
├── main.py                    # Application entry point & service initialization
├── requirements.txt           # Project package dependencies
└── README.md                  # System documentation and instructions