from sqlalchemy import Column, Integer, String, Text

from database import Base


class CityDB(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    additional_info = Column(Text())
