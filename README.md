# FastAPI city temperature management

## Description
FastAPI application that manages city data and their corresponding temperature data.

The application has two main components (apps):
- A CRUD (Create, Read, Update, Delete) API for managing city data.
- An API that fetches current temperature data for all cities in the database and stores this data in the database.

### City Management
- `POST /cities`: Create a new city.
- `GET /cities`: Get a list of all cities.
- `GET /cities/{city_id}`: Get the details of a specific city.
- `PUT /cities/{city_id}`: Update the details of a specific city.
- `DELETE /cities/{city_id}`: Delete a specific city.

### Temperature Management
- `GET /temperatures`: Get a list of all temperature records.
- `GET /temperatures/?city_id={city_id}`: Get the temperature records for a specific city.
- `POST /temperatures/update`: Get the current temperature for all cities from [Weather API](https://www.weatherapi.com/docs/) and stores this data.


### Technologies Used
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- SQLite
- httpx


## Installing using GitHub
1) Open the command prompt/terminal on your machine.

2) Navigate to the project folder where you want to clone the repository
    ```
    cd /path/to/project
    ```
   
3) Clone project from GitHub.
    ```
    git clone <URL of GitHub repository>
    ```

4) Navigate to the project directory.
    ```
    cd <project directory>
    ```
   
5) Create a virtual environment.
    ```
    python -m venv venv
    ```
     
6) Activate the virtual environment.
   - Unix/Linux/macOS
      ```
      source venv/bin/activate
      ```
   - Windows
      ```
      .\venv\Scripts\activate
      ```
     
7) Install the requirements.
    ```
    pip install -r requirements.txt
    ```
   
8) Сreate a .env file with your parameters as a .env.sample file.
    
9) Set up the database. 
    ```
    alembic upgrade head
    ```  
   
10) Run the application.
    ```
    uvicorn main:app --reload
    ```