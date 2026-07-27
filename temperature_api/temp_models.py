from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from db.database import Base



class DBTemperature(Base):
    __tablename__ = "Temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("City.id"))
    date_time = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=True)
