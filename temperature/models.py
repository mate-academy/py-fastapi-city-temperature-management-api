from sqlalchemy import Column, Integer, ForeignKey, Float

from database import Base


class DBTemperature(Base):
    __tablename__ = "Temperature"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("City.id"))
    date_time = Column(Integer, index=True)
    temperature = Column(Float, index=True)