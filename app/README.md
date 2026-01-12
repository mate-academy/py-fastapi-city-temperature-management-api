## City Temperature Management API

This is a FastAPI application that manages city data and their corresponding temperature data. 

The application provides:

* CRUD operations for cities.
* Temperature tracking for cities by fetching data from an external weather service.
* History of recorded temperatures for each city.
* 
Table of Contents

* Installation
* Running the Application
* API Endpoints
* Design Choices
* Description
* Assumptions / Simplifications


## Installation

### Clone the repository:
```shell
git clone <repository_url>
cd py-fastapi-city-temperature-management-api
```


### Create and activate a virtual environment:

```shell
python -m venv venv
venv\Scripts\activate
```

### Install dependencies:

```shell
pip install -r requirements.txt
```

### Running the Application

```shell
uvicorn app.main:app --reload
```
