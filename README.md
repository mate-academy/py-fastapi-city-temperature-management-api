## City Temperature API

This is a FastAPI application that manages city data and their corresponding temperature data. The application have one main component (app):

1. A CRUD (Create, Read, Update, Delete) API for managing city data.
2. An API that fetches current temperature data for all cities in the database and stores this data in the database. This API give to possibility a list endpoint to retrieve the history of all temperature data.

## Stack technologies
1. Python 3.12 
2. SQLite 3 — Database.
3. SQLAlchemy — ORM library.
4. Alembic — A tool for managing database migrations.
5. Pydantic — Used for data validation.
6. Black — A code formatter.


## How to install
- git clone <repository-url>
- Create virtual environment with: `python -m venv .venv`
- Activate: `.venv/Scripts/activate`
- Install requirements: `pip install -r requirements.txt`
- Run local host: `uvicorn main:app --reload`

