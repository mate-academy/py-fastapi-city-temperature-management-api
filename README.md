## City Temperature Management API
This is a FastAPI application designed to manage city data and their corresponding temperature records. The application includes two main components:
1. City CRUD API - For managing information about cities.
2. Temperature API - For fetching and storing the current temperature for all cities in the database.

### Project Structure
- city: Handles CRUD operations for cities.
- temperature: Manages temperature records, including an async update function to fetch current temperatures.

### Requirements
- Python 3.x
- SQLite
- requirements.txt dependencies

### Installation and Running the Application
Install dependencies:
`pip install -r requirements.txt`

Set up the database: Run the following commands to apply migrations:
`alembic upgrade head`

Create .env file in the root directory and add your API key for weatherapi.com:
`API_KEY=your_api_key_here`

Run the application:
`uvicorn main:app --reload`

### Design Choices
- FastAPI Framework: Selected for its support of asynchronous functions, which is essential for efficient temperature data fetching.
- Async Temperature Update: Uses an async function to fetch current temperature data for multiple cities in parallel.
- Dependency Injection: Ensures modular, reusable code across endpoints.
- Separate Apps: The city and temperature components are split to maintain a clear separation of concerns and modularity.
