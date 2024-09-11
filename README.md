## Fastapi city temperature management API

## Running locally:
1. Clone the repository:
```
git clone https://github.com/Yuruch/fastapi-city-temperature-management-api.git
```
2. Navigate to the project directory:
```
cd fastapi-city-temperature-management-api
```
3. Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate
```
4. Install the required dependencies:
```
pip install -r requirements.txt
```
5. Create a .env file and define environmental variables following the example:
```
WEATHER_API_KEY=your_weather_api_key
WEATHER_API=https://api.weatherapi.com/v1/current.json
```
6. Set up the database:
```
alembic upgrade head
```
7. Run the development server:
```
uvicorn main:app --reload --log-level debug
```