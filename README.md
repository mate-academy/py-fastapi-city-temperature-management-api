# 🌆 City & Temperature Management API

## 📌 How to Run the Project

1. **Create a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```
3. **Run migrations**
```bash
alembic upgrade head
```
4**Run migrations**
```bash
uvicorn main:app --reload
```
### Environment Variables
**create a .env file in the root directory of the project with your API keys**
```bash
WEATHER_API_KEY=your_weatherapi_key_here
```


## 🗺️ API Endpoints

### Cities

| Method | Endpoint       | Description         |
|--------|----------------|-------------------|
| GET    | /city/         | Get all cities     |
| GET    | /city/{id}     | Get a single city by ID |
| PATCH  | /city/{id}     | Update a city by ID |

### Temperatures

| Method | Endpoint                 | Description                                               |
|--------|--------------------------|-----------------------------------------------------------|
| GET    | /temperatures/           | Get all temperature records; optional filter by `city_id` |
| GET    | /temperatures/{id}       | Get a single temperature record by its ID                 |
| POST   | /temperatures/           | Create a temperature record manually                      |
| POST   | /temperatures/update/    | Fetch current temperature for all cities and save records |

