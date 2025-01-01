# City Temperature Management API

This project is a FastAPI-based application that allows users to manage city data and retrieve temperature data for those cities using a third-party weather API. The application provides CRUD (Create, Read, Update, Delete) functionality for city management and a mechanism to fetch and store temperature data for cities.

---

## **Instructions to Run the Application**

### **Setup Steps**

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/BitRxp/py-fastapi-city-temperature-management-api.git
   cd py-fastapi-city-temperature-management-api

2. **Set Up Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # For Windows: .venv\Scripts\activate
   
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt

4. **Configure Environment Variables: Create a .env file in the project root and include the following:**
   ```bash
   API_WEATHER=<your_weather_api_key>

5. **Apply Database Migrations: Initialize Alembic for migrations:**
   ```bash
   alembic init alembic
   ```
   Create migration scripts and apply:
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head

6. **Run the Application:**
   ```bash
   uvicorn main:app --reload


## **Key Endpoints**

### **City Management Endpoints**

- **`POST /cities/`**  
  Add a new city to the database.

- **`GET /cities/`**  
  Retrieve a list of all cities.

- **`PUT /cities/{city_id}`**  
  Update details of a specific city by its ID.

- **`DELETE /cities/{city_id}`**  
  Delete a specific city by its ID.

### **Temperature Management Endpoints**

- **`POST /temperatures/update`**  
  Fetch and update city temperatures.

- **`GET /temperatures/`**  
  Retrieve all temperature records.

- **`GET /temperatures/{city_id}`**  
  Retrieve all temperature records.