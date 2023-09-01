# Temperature Tracker

Temperature Tracker is an API that manages temperature records for various cities worldwide. You can add cities to the database and use the temperature update endpoint to keep the temperature data up-to-date.

## Installation and Usage

Follow these steps to set up and run the Temperature Tracker API on your local machine:
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/temperature-tracker.git
   cd temperature-tracker
2. Rename `.env.smpl` to `.env` and replace `WEATHER_TOKEN` with your actual WeatherAPI token.
3. Set up a virtual environment (Windows):
    ```sh
    python -m venv venv
    venv\Scripts\activate
4. Install required dependencies:
    ```sh
   `pip install -r requirements.txt`
5. Initialize the database: 
   ```sh
   `alembic upgrade head`
6. Start app 
    ```sh
    `uvicorn main:app`

7. Access the API using a tool like [Postman](https://www.postman.com/) at http://127.0.0.1:8000.

8. To stop the app, press `ctrl + c` or close the terminal.
## Usage
#### Base URL
* `127.0.0.1:8000`
#### City endpoints
* GET `/cities/` - Retrieve a list of cities with additional info
* POST `/cities/` _with provided `name` and `additional_info`_ - add city to the database
* DEL `/cities/1` - delete city with ID 1 from the database.

#### Temperature endpoints
* GET `/temperatures/` - list of **all** Temperature records
* GET `/temperatures/` _with `id` provided_ - list of **city with this id** Temperature records
* POST `/temperatures/update/` - update Temperature records for **all cities** in the database