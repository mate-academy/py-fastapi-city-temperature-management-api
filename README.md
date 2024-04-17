Introduction
This FastAPI project offers a straightforward and effective way to handle city data and their temperature records. Whether you're retrieving, adding, updating, or deleting city entries and their temperature data, this user-friendly API makes it a breeze.

Features
Ease of Use: Enjoy a simple and intuitive interface for managing city and temperature data.
Full Control: Perform a variety of operations, including retrieval, addition, updating, and deletion of city entries and temperature records.
Validation: FastAPI assures that input data is carefully validated to ensure accuracy and consistency.
API Documentation: Access comprehensive API documentation for seamless integration and usage.
Bonus
Asynchronous Requests for External API Updates: In this Temperature management API, a powerful feature was implemented that allows for asynchronous requests to an external API when updating temperature data for all cities. This feature ensures efficient and speedy retrieval of current temperature information, enhancing the overall performance and responsiveness of our application.
Description
Our project consists of two main applications:

City CRUD API
The City CRUD API enables users to perform basic CRUD operations on city data. It allows users to create, retrieve, update, and delete city entries. This API was designed to be intuitive and easy to use, ensuring seamless management of city information.

Temperature API
The Temperature API is responsible for managing temperature records associated with cities. It provides endpoints to fetch temperature data for specific cities and update temperature records. This API was implemented to fetch current temperature data from external sources and store it efficiently in our database.

Design Choices
FastAPI
FastAPI was chosen for its high performance, asynchronous capabilities, and automatic API documentation generation. FastAPI allows to build scalable and efficient web applications with minimal effort.

SQLAlchemy
For database management, SQLAlchemy was opted due to its powerful ORM capabilities and support for multiple database backends. Using SQLAlchemy simplifies database interactions and ensures data integrity and consistency.

Alembic
Alembic is used for database migrations in this project. It provides a robust framework for managing database schema changes over time. With Alembic, it's possible to easily version-control the database schema and apply migrations as needed, ensuring smooth and reliable database upgrades across different environments.

Pydantic
Pydantic is used for data validation and serialization. By defining Pydantic models for our data structures, we ensure that input data is validated before processing, reducing the risk of errors and improving overall reliability.

Installation
Clone the project on your local machine
git clone git@github.com:IKruglyak/py-fastapi-city-temperature-management-api.git
Open it in your IDE
python -m venv venv
source venv/bin/activate  # for linux/macos
venv\Scripts\activate  # for windows
pip install -r requirements.txt
Run the server and explore!
uvicorn main:app --reload
API Endpoints
For a detailed list of available endpoints and their functionalities, check out API documentation. You can typically find it at /docs after starting the app.

Good luck!