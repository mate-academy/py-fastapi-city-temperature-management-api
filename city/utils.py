from typing import Callable
from functools import wraps
from fastapi import HTTPException, status

from .schemas import City


def ensure_city_exist(func: Callable) -> Callable:
    """Decorator for verifying if DBCity object is returned else error"""
    @wraps(func)
    async def wrapper(*args, **kwargs) -> City | HTTPException:
        city = await func(*args, **kwargs)
        if city:
            return city
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no city like that"
        )
    return wrapper
