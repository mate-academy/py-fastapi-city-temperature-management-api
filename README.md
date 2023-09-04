## FastAPI City and Temperature Management API
This FastAPI application manages city data and their corresponding temperature data. It consists of two main components: a CRUD API for managing city data and an API for fetching and storing current temperature data for cities

### Installation
If you are using PyCharm - it may propose you to automatically create venv for your project and install requirements in it, but if not:
```
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
```
Apply migrations
```
alembic upgrade head
```
Run hte app
```
uvicorn main:app --reload
```

### Endpoints
http://127.0.0.1:8000/docs/ - documentation where you can find all endpoints


### Configuration
Create a .env file in the project root based on the provided .env.example file.


### Technology used
- FastAPI: A modern, fast (high-performance) web framework for building APIs with Python.
- SQLAlchemy: A popular SQL toolkit and Object-Relational Mapping (ORM) library.
- Pydantic: Data validation and parsing library.
- Uvicorn: ASGI server for running FastAPI applications.



