# Py FastAPI City Temperature Management API

This application is an API for managing city temperatures using FastAPI.

# Installation

# 1. Clone the repository:

```bash
git clone https://github.com/yourusername/py-fastapi-city-temperature-management-api.git

# 1. Navigate to the project directory:
   cd py-fastapi![img.png](img.png)-city-temperature-management-api

# 2. Install dependencies:
   pip install -r requirements.txt

# Usage

# Creating a City:
   POST /cities/

Creates a new city with the provided data.

Example Request:

{
  "name": "New York",
  "additional_info": "Capital city of the United States"
}

Example Response:

{
  "id": 1,
  "name": "New York",
  "additional_info": "Capital city of the United States"
}


# Getting a List of Cities

GET /cities/

Retrieves a list of cities with optional pagination.

Example Response:

[
  {
    "id": 1,
    "name": "New York",
    "additional_info": "Capital city of the United States"
  },
  {
    "id": 2,
    "name": "Los Angeles",
    "additional_info": "City in California"
  }
]


# Getting a City by ID

GET /cities/{city_id}

Retrieves a city by its identifier.

Example Response:

{
  "id": 1,
  "name": "New York",
  "additional_info": "Capital city of the United States"
}


# Deleting a City by ID

DELETE /cities/{city_id}

Deletes a city by its identifier.

Example Response:

{
  "detail": "City deleted"
}

created in pain but with inspiration)))
