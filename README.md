# FastAPI city temperature management service
## Online management system for city temperature

## Setup and Local Installation

### To set up and run the project locally, follow these steps:

#### 1.  Clone the repository:

```python
git clone https://github.com/OleksandrYanchuk/py-fastapi-city-temperature-management-api.git
```
#### 2. Open the folder:
```python
cd py-fastapi-city-temperature-management-api
```
#### 3. Create a virtual environment:
```python
python -m venv venv
```
#### 4. Activate the virtual environment:
   
##### - For Windows:
```python
venv\Scripts\activate
```
##### -	For macOS and Linux:
```python
source venv/bin/activate
```

#### 5. For run application manually make next steps:

```python
pip install -r requirements.txt
```
```python
alembic upgrade head
```
#### 6.Run server:
```python
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
#### 7. Open your web browser and go to http://localhost:8000 to access the application.

#### 8. Use next link for see docs:
```python
http://127.0.0.1:8000/docs
```
