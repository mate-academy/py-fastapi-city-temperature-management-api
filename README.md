## This is an API that allows to add cities and monitor temperature for them.
### As source of temperature data is used [Weather API](https://www.weatherapi.com/).

## Features
- Add city
- Read city by id
- Read all cities
- Update city
- Delete city
- Read all temperatures for all cities
- Read all temperatures for city
- Fetch new temperature for cities

### Installation
Python should be already installed
```bash
git clone https://github.com/MarianKovalyshyn/py-fastapi-city-temperature-management-api.git
cd py-fastapi-city-temperature-management-api/
python -m venv venv
source venv/bin/activate (MacOS)
venv\Scripts\activate (Windows)
pip install -r requirements.txt
uvicorn main:app --reload
```


