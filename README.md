### Installation

 #### Install virtual environment
	
	1. python -m venv venv
	2. source venv/bin/activate
	
 #### Install all the necessary requirements
 
	pip install requirements.txt
 
 #### Make migrations & create tables
 
	1. alembic revision --autogenerate -m "Create_city_&_temperature_table"
	2. alembic upgrade head
 
 #### Run server

***
### Endpoints
City:
- `GET /cities/`  -  Get a list of all cities (check docs if you need some limit and skip)
- `POST /cities/` - Create a new city
- `GET /cities/{city_id}/` - Get the details of a specific city
- `PUT /cities/{city_id}/` -  Update the details of a specific city
- `DELETE /cities/{city_id}/` - Delete a specific city

Temperature:
- `POST /temperatures/update/` - Retrieving temperature data from the Openweather API for all cities in your database.
- `GET /temperatures/` - Get a list of all temperature records
- `GET /temperatures/{city_id}/` - Get the temperature records for a specific city