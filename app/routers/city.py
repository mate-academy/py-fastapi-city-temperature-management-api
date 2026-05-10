from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_database

from app.city.models import City
from app.city import crud
from app.city import schemas
from app.city import utils


router = APIRouter()


def city_data_db_params(
	city_data: schemas.CityBase,
	db: AsyncSession = Depends(get_database)
) -> dict:
	return {"db": db, "city_data": city_data}


def city_id_db_params(
	city_id: int,
	db: AsyncSession = Depends(get_database)
) -> dict:
	return {"city_id": city_id, "db": db}


CityDataDbParams = Annotated[dict, Depends(city_data_db_params)]
CityIdDbParams = Annotated[dict, Depends(city_id_db_params)]


@router.get("/cities", response_model=list[schemas.CityList])
async def read_cities(db: AsyncSession = Depends(get_database)) -> list[City]:
	return await crud.get_all_cities(db)


@router.get("/cities/{city_id}", response_model=schemas.CityList)
async def read_city(params: CityIdDbParams) -> City:
	return await utils.handle_city_not_found(
		db=params["db"],
		city_id=params["city_id"]
	)


@router.post("/cities", response_model=schemas.CityCreate)
async def write_city(params: CityDataDbParams) -> dict:
	await utils.handle_city_exists(
		db=params["db"],
		city_data=params["city_data"]
	)

	return await crud.create_city(params["db"], params["city_data"])


@router.put("/cities/{city_id}", response_model=schemas.CityUpdate)
async def modify_city(city_id: int, params: CityDataDbParams) -> dict:
	await utils.handle_city_not_found(
		db=params["db"],
		city_id=city_id
	)
	await utils.handle_city_exists(
		db=params["db"],
		city_id=city_id,
		city_data=params["city_data"]
	)

	return await crud.update_city(params["db"], params["city_data"], city_id)


@router.delete("/cities/{city_id}")
async def remove_city(params: CityIdDbParams) -> None:
	await utils.handle_city_not_found(
		db=params["db"],
		city_id=params["city_id"]
	)

	return await crud.delete_city(params["db"], params["city_id"])
