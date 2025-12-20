from sqlalchemy.orm import Session
import models

def get_cities(db: Session):
    return db.query(models.City).all()

def delete_city(db: Session, city_id: int):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if db_city:
        db.delete(db_city)
        db.commit()
        return True
    return False
