from fastapi import status


class AppException(Exception):
    """Base exception for all domain errors"""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Internal Server Error"


class CityNotFound(AppException):
    """Raised when the specified city ID does not exist."""

    status_code = status.HTTP_404_NOT_FOUND
    detail = "City not found"


class CityAlreadyExists(AppException):
    """Raised when attempting to create a city with a duplicate name."""

    status_code = status.HTTP_409_CONFLICT
    detail = "City with that name already exists"


class WeatherApiError(AppException):
    """Raised when the weather API is unreachable or all requests failed."""

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    detail = "Weather service is temporarily unavailable"
