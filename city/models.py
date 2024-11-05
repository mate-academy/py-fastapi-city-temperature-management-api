from sqlalchemy import Column, Integer, String
from database import Base


class City(Base):
    __tablename__ = "City"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    additional_info = Column(String)
