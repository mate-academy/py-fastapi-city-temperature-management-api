from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from engine import session_manager

from city import schemas, crud

router = APIRouter()


@router.get(path="/cities/",
            response_model=list[schemas.CityBase],
            tags=["Cities"])
async def read_all_cities(
        session: AsyncSession = Depends(session_manager),
        skip: int = 0,
        limit: int = 10):
    get_city_list = await crud.get_all_cities(session=session,
                                              skip=skip,
                                              limit=limit)
    if not get_city_list:
        raise HTTPException(status_code=404,
                            detail="DataBase is empty")
    return get_city_list


@router.get(path="/cities/{city_name}",
            response_model=schemas.CityBase,
            tags=["Cities"])
async def read_specific_city(
        city_name: str,
        session: AsyncSession = Depends(session_manager)):
    check_city_name = await crud.get_city_by_name(
        session=session,
        city_name=city_name
    )
    if check_city_name is None:
        raise HTTPException(
            status_code=404,
            detail="City with such name was not found"
        )
    return check_city_name


@router.post(path="/cities/",
             response_model=schemas.City,
             tags=["Cities"])
async def create_city(
        city: schemas.CityBase,
        session: AsyncSession = Depends(session_manager)):
    """
       note that for smooth work of the weather API :

       - **use "USA"**: for the United States of America
       - **use "UK"**: for the United Kingdom of Great Britain
       - **for other countries**: use full country names
       """
    check_city_name = await crud.get_city_by_name(session=session,
                                                  city_name=city.name)
    if check_city_name:
        raise HTTPException(
            status_code=400,
            detail="City with such name is present in the Database"
        )
    return await crud.create_new_city(
        session=session,
        city=city)


@router.put(path="/cities/{city_name}",
            tags=["Cities"])
async def rewrite_city_info(
        city_name: str,
        city: schemas.CityBase,
        session: AsyncSession = Depends(session_manager)):
    """
       note that for smooth work of the weather API :

       - **use "USA"**: for the United States of America
       - **use "UK"**: for the United Kingdom of Great Britain
       - **for other countries**: use full country names
       """
    check_city_name = await crud.get_city_by_name(
        session=session,
        city_name=city_name
    )
    if check_city_name is None:
        raise HTTPException(status_code=404,
                            detail="No Such city in the Database")
    return await crud.update_city_info(
        session=session,
        city=city,
        city_name=city_name)


@router.delete(path="/cities/{city_name}",
               tags=["Cities"])
async def delete_city(
        city_name: str,
        session: AsyncSession = Depends(session_manager)):
    check_city_by_name = await crud.get_city_by_name(session=session,
                                                     city_name=city_name)
    if check_city_by_name is None:
        raise HTTPException(status_code=404,
                            detail="No such city in the Database")
    return await crud.delete_city(
        session=session,
        city_name=city_name)
