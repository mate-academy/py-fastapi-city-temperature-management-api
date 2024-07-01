from fastapi import HTTPException


class CityAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Such name for Temperature already exists")


class CityNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Temperature not found")
