from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.database import BaseModel


class City(BaseModel):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(63), unique=True, nullable=True)
    additional_info = Column(String(255), nullable=True)

    city = relationship("Temperature", backref="cities")
