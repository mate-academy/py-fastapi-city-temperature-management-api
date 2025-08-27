from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from temperature.models import Temperature # noqa

from database import Base


class City(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(63), unique=True, nullable=False)
    additional_info = Column(String(511), nullable=True)

    temperatures = relationship(
        "Temperature", back_populates="city", passive_deletes=True
    )
