from sqlalchemy.orm import Session
from temperature import temp_models, schemas


async def get_all_temperature(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Temperature).offset(skip).limit(limit).all()


async def get_temperature_by_id(db: Session, temperature_id: int):
    return db.query(models.Temperature).filter(models.Temperature.id == temperature_id).first()


async def create_temperature(db: Session, temperature: schemas.TemperatureCreate):
    db_temperature = models.Temperature(
        city_id=temperature.city_id,
        date_time=temperature.date_time,
        temperature=temperature.temperature
    )
    db.add(db_temperature)
    await db.commit()
    await db.refresh(db_temperature)
    return db_temperature


async def update_temperature(db: Session, temperature_id: int, temperature: schemas.TemperatureUpdate):
    db_temperature = await db.query(models.Temperature).filter(models.Temperature.id == temperature_id).first()
    if db_temperature:
        db_temperature.city_id = temperature.city_id
        db_temperature.date_time = temperature.date_time
        db_temperature.temperature = temperature.temperature
        await db.commit()
        await db.refresh(db_temperature)
    return db_temperature


async def delete_temperature(db: Session, temperature_id: int):
    db_temperature = await db.query(models.Temperature).filter(models.Temperature.id == temperature_id).first()
    if db_temperature:
        await db.delete(db_temperature)
        await db.commit()
    return db_temperature
