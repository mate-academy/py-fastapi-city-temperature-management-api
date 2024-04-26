from typing import Any
from fastapi import HTTPException, status, Response
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def get_city_list(db: AsyncSession) -> list[models.DbCity]:
    query = select(models.DbCity)
    city_list = await db.execute(query)

    return city_list.scalars().all()


async def get_city_detail(db: AsyncSession, city_id: int) -> models.DbCity:
    query = select(models.DbCity).filter(models.DbCity.id == city_id)
    result = await db.execute(query)
    city = result.scalar_one_or_none()
    if city:
        return city
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"City with id {city_id} not found",
    )


async def create_city(
    db: AsyncSession, city_create: schemas.CityCreate
) -> dict[str, Any]:

    try:
        query = insert(models.DbCity).values(
            name=city_create.name,
            additional_info=city_create.additional_info,
        )

        result = await db.execute(query)
        await db.commit()
        resp = {**city_create.model_dump(), "id": result.lastrowid}

        return resp

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City with this name already exists.",
        )

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}"
        )


async def update_city(
    db: AsyncSession, city_id: int, city_update: schemas.CityCreate
) -> schemas.CityCreate:
    city = await db.get(models.DbCity, city_id)

    if city:
        query = (
            update(models.DbCity)
            .where(models.DbCity.id == city_id)
            .values(
                name=city_update.name,
                additional_info=city_update.additional_info,
            )
        )
        await db.execute(query)
        await db.commit()
        return city_update

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"City with id {city_id} not found",
    )


async def delete_city(db: AsyncSession, city_id: int) -> Response:
    city = await db.get(models.DbCity, city_id)

    if city:
        query = delete(models.DbCity).where(models.DbCity.id == city_id)
        await db.execute(query)
        await db.commit()
        return Response(
            status_code=status.HTTP_200_OK, content=f"Deleted: {city.name}"
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"City with id {city_id} not found",
    )
