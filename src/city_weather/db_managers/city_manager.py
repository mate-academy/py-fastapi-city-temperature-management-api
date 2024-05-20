from sqlalchemy.exc import NoResultFound
from sqlalchemy import select
from src.city_weather.db_managers.abstract_manager import AbstractDBManager
from src.city_weather.models import City
from src.database import SessionLocal
from src.exceptions import ObjectNotFound, ValidationError, ErrorSaving


class CityDBManager(AbstractDBManager):
    model = City

    async def create_new_item(self, data):
        await self.validate_item(data)
        data = data.model_dump()
        try:
            async with SessionLocal() as session:
                new_item = self.model(**data)
                session.add(new_item)
                await session.commit()
                return new_item
        except Exception as e:
            raise ErrorSaving(detail=str(e))

    async def update_item(self, data):
        item = await self.get_item_by_id(data.id)
        data = data.model_dump()
        try:
            async with SessionLocal() as session:
                for attr, value in data.items():
                    setattr(item, attr, value)
                await session.commit()
                return item
        except Exception as e:
            raise ErrorSaving(detail=str(e))

    async def get_item_by_id(self, item_id: int):
        async with SessionLocal() as session:
            try:
                city = await session.execute(
                    select(self.model)
                    .where(self.model.id == item_id)
                )
                result = city.scalar_one()
            except NoResultFound:
                raise ObjectNotFound(detail="No city found with such id")
            else:
                return result

    async def delete_item(self, item_id: int):
        item = await self.get_item_by_id(item_id)
        async with SessionLocal() as session:
            await session.delete(item)
            await session.commit()
            return item

    async def validate_item(self, data):
        await self.check_name_country(data)

    async def check_name_country(self, data):
        async with SessionLocal() as session:
            try:
                city = await session.execute(
                    select(self.model)
                    .where(self.model.name == data.name)
                    .where(self.model.country == data.country)
                )
                result = city.scalar_one()
            except NoResultFound:
                pass
            else:
                raise ValidationError(detail=f"This city is already exist. ID: {result.id}")
