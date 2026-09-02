# City Temperature Management API

A FastAPI application that provides a CRUD API for managing city data and an automated endpoint to fetch and store current temperatures for all registered cities using an external weather service.

## Instructions on how to run the application

1. **Clone the repository and navigate to the project directory:**
   ```bash
   git clone <your-repo-url>
   cd py-fastapi-city-temperature-management-api
   
2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt


4. **Apply database migrations:**

   ```bash
   alembic upgrade head


5. **Run the FastAPI server:**

   ```bash
   uvicorn main:app --reload


6. **Access the API Documentation:**
Open your browser and navigate to http://127.0.0.1:8000/docs to test the endpoints via Swagger UI.

Brief explanation of design choices
Framework: FastAPI was chosen for its high performance, automatic interactive API documentation (Swagger UI), and built-in support for asynchronous programming.

Database & ORM: SQLite was used as the database for its simplicity and portability, managed through SQLAlchemy ORM. Alembic was integrated for reliable database migrations.

External API Integration: httpx is used for asynchronous HTTP requests to fetch weather data without blocking the main event loop. The free wttr.in API is used as the data source.

Error Handling: Added try-except blocks and detailed logging during the batch temperature update process. If one city fails to update, the loop continues for the remaining cities, and failed cities are reported in the API response.