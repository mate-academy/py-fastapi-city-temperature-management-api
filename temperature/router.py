from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import crud
from dependencies import get_db, Pagination, pagination_params
from temperature.schemas import TemperatureRead

router = APIRouter()


class UpdateTemperaturesResponse(BaseModel):
    message: str = Field(..., description="Result message")
    updated: int = Field(..., description="Number of cities successfully updated")
    unupdated: int = Field(..., description="Number of cities that failed to update")
    error: list[str] = Field(
        ..., description="List of errors encountered during update"
    )


@router.get("/temperatures", response_model=list[TemperatureRead])
async def list_temperatures(
    db: Annotated[AsyncSession, Depends(get_db)],
    pagination: Annotated[Pagination, Depends(pagination_params)],
    city_id: int | None = None,
) -> list[TemperatureRead]:
    if city_id:
        temperature = await crud.get_temperature_by_city_id(
            db=db,
            city_id=city_id,
            skip=pagination.skip,
            limit=pagination.limit,
        )
        return temperature

    return await crud.get_all_temperatures(
        db=db, skip=pagination.skip, limit=pagination.limit
    )


@router.post(
    "/temperatures/update",
    summary="Update temperatures for all cities",
    description=(
        "Fetches current temperatures for all cities from the external weather API, "
        "updates existing records, and returns statistics about successful and failed updates."
    ),
    response_description="Statistics about the temperature update process",
)
async def update_all_temperatures(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UpdateTemperaturesResponse:
    updated_count, errors = await crud.update_all_temperatures(db=db)

    return UpdateTemperaturesResponse(
        message=(
            "Temperatures updated successfully"
            if not errors
            else "Temperatures updated partially"
        ),
        updated=updated_count,
        unupdated=len(errors),
        error=errors,
    )
