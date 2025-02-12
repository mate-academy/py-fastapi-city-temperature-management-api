from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from city_temperature_api.database.session.engine import Base


class City(Base):

    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    additional_info = Column(String)

    temperatures = relationship(
        "Temperature",
        back_populates="city",
        lazy="selectin"
    )
