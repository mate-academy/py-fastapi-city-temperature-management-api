# City temperature management API

An API that retrieves current temperature data for all cities within the database and subsequently stores this information. Additionally, the API offers an endpoint for retrieving the historical temperature data for all cities.






## Prepare the project
1. Clone repo
    ```
    git clone https://github.com/Daniil-Pankieiev/py-fastapi-city-temperature-management-api.git
    ```
2. Open the project folder in your IDE
3. Open a terminal in the project folder
4. Create a branch for the solution and switch on it
    ```
    git checkout -b develop
    ```
5. Create venv
    ```
    python -m venv venv
    venv\Scripts\activate (on Windows)
    source venv/bin/activate (on macOS)
    pip install -r requirements.txt
    ```

6. For run application manually make next steps:

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