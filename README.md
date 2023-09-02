# City temperature management API


Project of "City temperature management API". For online managing cities and current temperature in it. Written on FastAPI


## Installing

Use this commands for installation of this project on your localhost

```shell
git clone https://github.com/Roman28101/py-fastapi-city-temperature-management-api
cd py-fastapi-city-temperature-management-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
* create .env file in main directory
* set api key for your weather service into it (use .env.sample for reference)

```
alembic upgrade head
uvicorn main:app --reload  
```


## Get access to project

* follow to http://127.0.0.1:8000/docs 
* POST /cities: Create a new city.
* GET /cities: Get a list of all cities.
* DELETE /cities/{city_id}: Delete a specific city.
* POST /temperatures/update: Update temperature info for created cities
* GET /temperatures: Get a list of all temperature records.
* GET /temperatures/?city_id={city_id}: Get the temperature records for a specific city.
