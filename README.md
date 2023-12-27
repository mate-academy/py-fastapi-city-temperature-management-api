# FastAPI city temperature management API
## Online management system for city temperature

FastAPI application that manages city data and their corresponding temperature data. The application has two main components (apps):

1. A CRUD (Create, Read, Update, Delete) API for managing city data.
2. An API that fetches current temperature data for all cities in the database and stores this data in the database. This API also provides a list endpoint to retrieve the history of all temperature data.

## Prepare the project
1. Clone repo
    ```
    git clone https://github.com/YuliaHladyshkevych/py-fastapi-city-temperature-management-api.git
    ```
    - You can get the link by clicking the `Clone or download` button in your repo
1. Open the project folder in your IDE
1. Open a terminal in the project folder
1. Create a branch for the solution and switch on it
    ```
    git checkout -b develop
    ```
    - You can use any other name instead of `develop`
1. If you are using PyCharm - it may propose you to automatically create venv for your project 
    and install requirements in it, but if not:
    ```
    python -m venv venv
    venv\Scripts\activate (on Windows)
    source venv/bin/activate (on macOS)
    pip install -r requirements.txt
    ```

1. For run application manually make next steps:

```python
pip install -r requirements.txt
```
```python
alembic upgrade head
```
7. Run server:

```python
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
8. Open your web browser and go to http://localhost:8000 to access the application.
