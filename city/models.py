from sqlalchemy import Column, Integer, String

from database import Base


class CityModel(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    additional_info = Column(String)
