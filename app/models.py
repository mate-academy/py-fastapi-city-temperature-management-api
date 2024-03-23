from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, index=True)  # noqa:VNE003
    name = Column(String, index=True)
    additional_info = Column(String)
    temperatures = relationship('Temperature',
                                back_populates='city')


class Temperature(Base):
    __tablename__ = 'temperatures'

    id = Column(Integer, primary_key=True, index=True)  # noqa:VNE003
    city_id = Column(Integer, ForeignKey('cities.id'))
    date_time = Column(DateTime)
    temperature = Column(Float)
    city = relationship('City',
                        back_populates='temperatures')
