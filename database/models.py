from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float

from database.engine import Base


class DBCity(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    additional_info = Column(String, nullable=True)


class DBTemperature(Base):
    __tablename__ = 'temperatures'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    date_time = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=False)
