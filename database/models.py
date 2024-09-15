from sqlalchemy import Integer, String, Column, ForeignKey, DateTime, Float

from database.engine import Base


class City(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    additional_info = Column(String(255), nullable=True)


class Temperature(Base):
    __tablename__ = "temperature"
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("city.id"), nullable=False)
    date_time = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=False)
