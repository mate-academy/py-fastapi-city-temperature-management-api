from typing import Generic, Type, TypeVar, List, Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app import models, schemas
from app.database import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            setattr(db_obj, field, obj_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int) -> Optional[ModelType]:
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj


class CRUDCity(CRUDBase[models.City, schemas.CityCreate, schemas.CityUpdate]):
    def get_by_name(self, db: Session, name: str) -> Optional[models.City]:
        return db.query(self.model).filter(models.City.name == name).first()


class CRUDTemperature(CRUDBase[models.Temperature, schemas.TemperatureBase, schemas.TemperatureBase]):
    def create_record(self, db: Session, city_id: int, temp: float) -> models.Temperature:
        db_obj = self.model(city_id=city_id, temperature=temp)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_city(self, db: Session, city_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[models.Temperature]:
        query = db.query(self.model)
        if city_id:
            query = query.filter(models.Temperature.city_id == city_id)
        return query.offset(skip).limit(limit).all()


city = CRUDCity(models.City)
temperature = CRUDTemperature(models.Temperature)
