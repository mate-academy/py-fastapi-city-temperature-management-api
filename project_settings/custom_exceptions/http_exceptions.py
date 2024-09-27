from fastapi import HTTPException


class CityNotFoundException(HTTPException):
    def __init__(self, city_id: int) -> None:
        super().__init__(
            status_code=404,
            detail=f"City with id {city_id} not found"
        )
