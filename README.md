# City Temperature Management API
This project is built on FastAPI and provides functionalities related to managing cities and temperature records.

To clone this project from GitHub, follow these steps:
1. Open your terminal or command prompt.
2. Navigate to the directory where you want to clone the project.
3. Clone repo:
```shell
git clone https://github.com/DmytroHlazyrin/py-fastapi-city-temperature-management-api.git
```
4. Go to directory:
```shell
cd py-fastapi-city-temperature-management-api
```
5. Create virtual environment:
```shell
python -m venv venv
venv\Scripts\activate #for Windows
source vevn/bin/activate #for Unix
```
4. Install requirements:
```shell
pip install -r requirements.txt
```
5. You should register on weatherapi.com and get your API_KEY
6. Create .env file with your API_KEY. There is env.sample for you.
## Adding Migrations
Execute the following commands to create and run migration with alembic:
```shell
alembic revision --autogenerate -m "initial_migrations"
alembic upgrade head
```
## Running the Server
To run the server execute the following command:
```shell
uvicorn main:app --reload
```
## Endpoints
You can explore all the endpoints on ```127.0.0.1:8000/docs``` endpoint.
### City
* ```GET /cities```: Get a list of all cities.
* ```POST /cities```: Create a new city.
* ```GET /cities/{city_id}```: Get details of a specific city.
* ```PUT /cities/{city_id}```: Update a specific city.
* ```DELETE /cities/{city_id}```: Delete a specific city.
### Temperature
* ```POST /temperatures/update```: Fetch and create/update temperature data for all cities.
* ```GET /temperatures```: Get a list of all temperature records.
* ```GET /temperatures/?city_id={city_id}```: Get temperature records for a specific city.
