### City Model

The `City` model is defined with the following fields:

- `id`: A unique identifier for the city.
- `name`: The name of the city.
- `additional_info`: Any additional information about the city.

### Temperature Model

The `Temperature` model is defined with the following fields:

- `id`: A unique identifier for the temperature record.
- `city_id`: A reference to the city.
- `date_time`: The date and time when the temperature was recorded.
- `temperature`: The recorded temperature.

### Endpoints
# City
1. **GET /city/list/**:
2. **GET /city/{city_id}/**:
3. **POST /city/create/**:
4. **PUT /city/{city_id}/update/**
5. **DELETE /city/cities/{city_id}/**

# Temperature
1. **GET /temperature/list/**: 
2. **GET /temperature/{city_id}**:

## Additional Requirements

- **Dependency Injection**: Used throughout the application to manage database sessions and other dependencies.
- **Project Organization**: The project follows FastAPI best practices for structuring the code.
