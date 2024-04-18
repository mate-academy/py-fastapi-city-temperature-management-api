# City Temperature API

API service for managing cities temperatures written on FastAPI.

# Installing using GitHub


```shell
git clone git@github.com:NataliiaKorzh/py-fastapi-city-temperature-management-api.git

python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt

```
Apply migrations
```shell
 alembic upgrade head 
 ```

# Run server

```shell
 uvicorn main:app --reload

```

For comfortable testing use 
```shell
http://127.0.0.1:8000/docs/
```
# API structure
``` GET /cities ``` Get a list of all cities

``` GET /cities/{city_id} ``` Get the details of a specific city

``` POST /cities ``` Create a new city

``` PUT /cities/{city_id} ``` Update the details of a specific city

``` DELETE /cities/{city_id} ``` Delete a specific city

``` GET /temperatures ``` Get a list of all temperature records

``` GET /temperatures/?city_id={city_id} ``` Get the temperature records for a specific city

``` POST /temperatures/update ``` Fetches the current temperature for all cities in the database from WeatherAPI
