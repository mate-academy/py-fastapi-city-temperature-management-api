# City Temperature Management API
This project is built on FastAPI and provides functionalities related to managing cities and temperature records.

To clone this project from GitHub, follow these steps:
1. Open your terminal or command prompt.
2. Navigate to the directory where you want to clone the project.
3. Run the following command:
```shell
git clone https://github.com/ArturPoltser/py-fastapi-city-temperature-management-api.git
cd py-fastapi-city-temperature-management-api
python -m venv venv
venv\Scripts\activate  #for MacOS/Linux use: source vevn/bin/activate
```
4. Install requirements:
```shell
pip install -r requirements.txt
```
5. You should register on weatherapi.com and get your WEATHER_API_KEY
6. Copy .env.sample and create .env file. After that you need to put your own WEATHER_API_KEY instead of default one.
## Adding Migrations
This project uses Alembic for managing database migrations. Execute the following commands to create and run migration:
```shell
alembic revision --autogenerate -m "initial_migrations"
alembic upgrade head
```
## Running the Server
To run the server execute the following command:
## Endpoints
I recommend you to interact with API from ```/docs``` endpoint.
### City App
* ```GET /cities```: Get a list of all cities.
* ```POST /cities```: Create a new city.
* ```GET /cities/{city_id}```: Get details of a specific city.
* ```PUT /cities/{city_id}```: Update a specific city.
* ```DELETE /cities/{city_id}```: Delete a specific city.
* ### Temperature App
* ```POST /temperatures/update```: Fetch and create/update temperature data for all cities.
* ```GET /temperatures```: Get a list of all temperature records.
* ```GET /temperatures/?city_id={city_id}```: Get temperature records for a specific city.

Feel free to reach out if you encounter any issues or have any questions. Happy coding!
