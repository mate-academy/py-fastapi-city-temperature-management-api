## City Weather Management API

### Tech Stack
- FastAPI asynchronous web framework
- SQLAlchemy 2.0 object relational mapper
- aiosqlite asynchronous driver for SQLite
- HTTPX asynchronous HTTP client for external requests
- Open-Meteo API free weather data provider

### How to Run the Application

Step 1 
- Set up the Virtual Environment
- Open your project folder in your IDE
- Open the integrated terminal
- Create a virtual environment by running 
```bash
python -m venv venv
```
- Activate the virtual environment
- For Windows PowerShell use 
```bash
.\venv\Scripts\activate
```
- For Windows Command Prompt use 
```bash
venv\Scripts\activate.bat
```
- For macOS or Linux use 
```bash
source venv/bin/activate
```
- You will know it works when you see venv at the beginning of your terminal line

Step 2 Install Dependencies
- Install all required libraries by running 
```bash
pip install -r requirements.txt
```
- Wait for the installation process to finish

Step 3 Start the Uvicorn Server
- Launch the development server with automatic reload by running 
```bash
uvicorn app.main:app --reload
```
- The application will automatically create the weather.db database file and initialize all required tables during this first startup

Step 4 Test via Swagger UI
- Open your browser and navigate to [http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs)
- This opens the interactive Swagger documentation where you can test all endpoints directly

### Design Choices and Assumptions

- Modular Architecture
The project is split into separate directories for cities and temperatures to keep the codebase clean organized and easy to maintain as it grows

- Fully Asynchronous
All database operations via aiosqlite and external API calls via HTTPX utilize async and await to prevent blocking the application event loop during network requests

- Cascade Deletion
Foreign key constraints are configured with ON DELETE CASCADE meaning that if a city is deleted from the database all its related temperature history records are automatically removed to prevent orphaned data

- Open-Meteo Integration
Since the Open-Meteo API requires precise latitude and longitude coordinates the temperature service uses a two-step process it first queries the Geocoding API to find the coordinates of a city by its name and then fetches the current temperature using those coordinates