## Instructions on how to run the application
1. Clone the repository:  
```bash
git clone https://github.com/samuel-edmund-morgan/py-fastapi-city-temperature-management-api.git
cd py-fastapi-city-temperature-management-api
```
2. Create and activate a virtual environment:
```python
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```
3. Install the dependencies:  
```python
pip install -r requirements.txt
```
4. Run the application:  
```bash
uvicorn main:app --reload
```
5. Access the API documentation: Open your browser and navigate to http://<your_ip>:8000/docs to see the interactive API documentation.

## Design Choices
- **FastAPI**: Chosen for its performance and ease of use in building APIs.
- **SQLAlchemy**: Used for ORM to interact with the SQLite database.
- **Pydantic**: Utilized for data validation and serialization.
- **Dependency Injection**: Implemented to manage database sessions and common parameters efficiently.
- **Asyncio**: Used for asynchronous operations to fetch temperature data concurrently.

## Assumptions and Simplifications
- **Database**: SQLite is used for simplicity and ease of setup.
- **Temperature API**: Assumes the external API for fetching temperature data is reliable and provides data in the expected format.
- **Error Handling**: Basic error handling is implemented, assuming that most errors will be related to network issues or invalid data.
- **Data Model**: Simplified data models for City and Temperature to focus on core functionality.