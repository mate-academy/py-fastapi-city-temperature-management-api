This FastAPI application provides a comprehensive solution for managing city and temperature data. It consists of two main components:

City CRUD API: Manage city data with endpoints to create, read, update, and delete city records. The City model includes fields for id, name, and additional_info, with data stored in a SQLite database.

Temperature API: Fetch and store current temperature data for cities using an external resource. It includes endpoints to update temperature records, retrieve all temperature data, and get records for specific cities. The Temperature model features id, city_id, date_time, and temperature.

# How to run

```sh
# Clone the repository
git clone https://github.com/Timur5050/Library-Service-project.git
# Change to the project directory
cd Library-Service-project
# Create a virtual environment
python -m venv venv
# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
# Install required packages
pip install -r requirements.txt
# Start uvicorn server and run FastApi project
python -m uvicorn main:app --reload
```

# How to use
### City CRUD API
```sh
# Create City: POST /cities
curl -X POST "http://localhost:8000/cities/" -H "Content-Type: application/json" -d '{"name": "CityName", "additional_info": "Info"}'
# Get All Cities: GET /cities
curl -X GET "http://localhost:8000/cities/"
# Get City Details: GET /cities/{city_id}
curl -X GET "http://localhost:8000/cities/{city_id}/"
# Update City: PUT /cities/{city_id}
curl -X PUT "http://localhost:8000/cities/{city_id}/" -H "Content-Type: application/json" -d '{"name": "UpdatedCity", "additional_info": "Updated Info"}'
# Delete City: DELETE /cities/{city_id}
curl -X DELETE "http://localhost:8000/cities/{city_id}/"
```
### Temperature API
```sh
# Update Temperature: POST /temperatures/update
curl -X POST "http://localhost:8000/temperatures/update/"
# Get All Temperatures: GET /temperatures
curl -X GET "http://localhost:8000/temperatures/"
# Get Temperatures by City: GET /temperatures/?city_id={city_id}
curl -X GET "http://localhost:8000/temperatures/{city_id}/"
```
