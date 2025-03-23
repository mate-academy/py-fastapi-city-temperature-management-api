# City temperature management API

## How to Run the Application

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

### Database Setup

Initialize the database with Alembic migrations:

```bash
alembic upgrade head
```

### Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Access the API documentation at `http://localhost:8000/docs`

## Design Choices

### Project Structure

The application follows a modular design with separate routers for cities and temperatures, following FastAPI best
practices

### Technology Choices

- **FastAPI**: Provides high performance, automatic documentation, and type validation
- **SQLAlchemy**: ORM for database interactions
- **Alembic**: Database migration tool
- **SQLite**: Lightweight database for simplicity
- **Pydantic**: Data validation and settings management

### Key Implementation Details

- Asynchronous temperature data fetching to improve performance
- Foreign key constraint with cascade delete between City and Temperature
- Dependency injection for database sessions
