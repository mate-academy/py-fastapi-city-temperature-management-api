# City Temperature Management FastAPI Application

This is a FastAPI application for managing city data and their corresponding temperature data

## Getting Started

### Prerequisites

- Python 3.x (with pip)
- SQLite (comes with Python by default)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/index.html)
- [Pydantic](https://docs.pydantic.dev/latest/)

## Features

- **City CRUD Operations**: Easily manage city data with Create, Read, Update, and Delete operations.
- **Temperature Data**: Fetch and store current temperature data for cities.
- **History Tracking**: Retrieve historical temperature data for analysis.
- **Flexible API Endpoints**: Comprehensive API endpoints for cities and temperature records.
- **Dependency Injection**: Utilize dependency injection for clean and organized code.
- **Database Integration**: Store data in an SQLite database using SQLAlchemy for efficient data management.
- **Asynchronous Fetching**: Fetch temperature data asynchronously for improved performance.
- **Documentation**: Clear and concise integrated documentation to help you get started quickly.
- **Contributor-Friendly**: Easy-to-understand codebase, welcoming contributions and improvements.

### Installation

1. Clone the repository:
```shell
git clone https://github.com/your-username/your-project.git
```
2. Create a virtual environment and activate it:
```shell
python -m venv venv
```

On Windows:
```shell
venv/scripts/activate
```

On MacOS:
```shell
source venv/bin/activate
```

Install requirements:
```shell
pip install -r requirements.txt
```
4. Set up environmental variables in .env, using [.env.sample](.env.sample) as an example.
For this, you need to register on [WheatherAPI website](https://openweathermap.org) to get your personal API Key.
5. Run migrations:
```shell
alembic upgrade head
```
6. Run the server:
```shell
uvicorn main:app --reload
```
> Note: if you want to see Swagger documentation, use this url: http://127.0.0.1:8000/docs

### Endpoints

**City**:
- `GET /cities/`: Get a list of all cities.
- `POST /cities/`: Create a new city.
- `GET /cities/{city_id}/`: Get the details of a specific city.
- `PUT /cities/{city_id}`: Update the details of a specific city.
- `DELETE /cities/{city_id}`: Delete a specific city.

**Temperature**:
- `GET /temperatures`: Get a list of all temperature records.
- `POST /temperatures/update`: Fetches current temperature data for all cities and stores it in the database.
- `GET /temperatures/?city_id={city_id}`: Get temperature records for a specific city.

## Design Choices

- The application uses FastAPI due to its simplicity, performance, and built-in support for asynchronous operations.
- SQLite is used for the database, as it's lightweight and comes with Python by default.
- SQLAlchemy is used as the ORM (Object-Relational Mapping) library to manage the database.

## Assumptions and Simplifications

- Proper authentication and authorization mechanisms are not implemented in this basic version.
- Error handling and validation could be further enhanced in a production environment.

## Contributing

Contributions are welcome! Feel free to open a pull request or submit issues for any improvements or features you'd like to add.
