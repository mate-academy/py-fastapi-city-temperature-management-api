from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.city.models import City
from app.city import schemas
from app.city import crud


async def handle_city_not_found(*, db: AsyncSession, city_id: int) -> City:
	city = await crud.get_city(db, city_id)

	if not city:
		raise HTTPException(
			status_code=400,
			detail="City not found"
		)

	return city


async def handle_city_exists(
	*,
	db: AsyncSession,
	city_data: schemas.CityBase,
	city_id: int = None,
) -> None:
	city = await crud.get_city_by_name(db, city_data.name)

	if (
		(city and city_id is not None and city_id != city.id)
		or (city and city_id != city.id)
	):
		raise HTTPException(
			status_code=400,
			detail="City with this name already exists"
		)
