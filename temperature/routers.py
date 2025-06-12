from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.post("/temperatures/update", response_model=list[schemas.Temperature])
async def update_all_temperature(db: AsyncSession = Depends(get_db)):
    try:
        updated = await crud.update_temperature(db=db)

        if not updated:
            raise HTTPException(
                status_code=404,
                detail="No temperatures updated, possibly no cities found"
            )

        return updated

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update temperatures: {str(e)}"
        )


@router.get("/temperatures", response_model=list[schemas.Temperature])
async def get_all_temperature(db: AsyncSession = Depends(get_db)):
    return await crud.get_list_of_temperature(db=db)


@router.get("/temperatures/{city_id}", response_model=schemas.Temperature)
async def get_temperature(city_id: int, db: AsyncSession = Depends(get_db)):
    db_temperature = await crud.get_temperature_by_id(db=db, city_id=city_id)
    if not db_temperature:
        raise HTTPException(status_code=404, detail="City not found")
    return db_temperature
