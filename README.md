### Temperature Management Project

This project is a FastAPI-based application for managing city temperature data. 
It fetches real-time weather information from an external API and stores it 
in a database using SQLAlchemy with asynchronous support. 
The application includes endpoints for retrieving and updating temperature records efficiently. 
Environment variables are managed using python-dotenv for secure configuration.

## Implemented
1. A CRUD (Create, Read, Update, Delete) API for managing city data.
2. An API that fetches current temperature data for all cities in the database 
and stores this data in the database.

## Design Choices
To enhance code readability and maintainability, the project is structured into multiple applications, 
with two separate models placed in different modules. This separation of concerns keeps the logic modular 
and easier to navigate.


### Additional Requirements

- Use dependency injection where appropriate.
- Organize your project according to the FastAPI project structure guidelines.

## Evaluation Criteria

The project meets the following standards:

Code Quality – The code is clean, readable, and well-organized, following best practices.
Error Handling – The application includes proper error handling to ensure stability and reliability.
Documentation – The project is well-documented, providing clear instructions and explanations for ease of use.

## Installation and Running Instructions

1. **Clone the repository**  
   ```sh
   git clone https://github.com/your-username/your-repository.git
   cd your-repository
   ```
   
2. **Create and activate a virtual environment**  
   ```sh
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate  # On Windows
   ```
   
3. **Install dependencies**  
   ```sh
    pip install -r requirements.txt
   ```
   
4. **Set up environment variables**  
   ```sh
    API_KEY=your_api_key
   ```
   
5. **Run database migrations**  
   ```sh
    alembic upgrade head
   ```
   
6. **Start the application**  
   ```sh
    uvicorn main:app --reload
   ```
   
7. **Access the API**

The application will be running at:
- API Documentation: http://127.0.0.1:8000/docs
- Alternative API UI: http://127.0.0.1:8000/redoc

## Technologies Used
- **Python 3.13+** – The core programming language used for backend development.  
- **FastAPI 0.115.8** – A high-performance web framework for building APIs with Python, offering automatic OpenAPI documentation.  
- **SQLAlchemy 2.0.37** – An ORM (Object-Relational Mapper) for interacting with the database using Python models.  
- **Alembic 1.14.1** – A lightweight database migration tool that manages schema changes seamlessly.  
- **PyMySQL 1.1.1** – A database system used for storing application data.  
- **Pydantic 2.10.6** – Provides data validation and serialization for FastAPI models.  
- **Async SQLAlchemy + AsyncSession** – Ensures efficient database operations using asynchronous processing.  
- **httpx 0.28.1** – An asynchronous HTTP client used for making external API requests.  
- **dotenv 1.0.1** – Used to manage environment variables securely.  
- **Uvicorn 0.34.0** – An ASGI server for running the FastAPI application.