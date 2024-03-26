from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    additional_info = Column(String, index=True)
    temperatures = relationship('Temperature', back_populates='city')


class Temperature(Base):
    __tablename__ = 'temperatures'
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey('cities.id'))
    date_time = Column(DateTime)
    temperature = Column(Float)
    city = relationship('City', back_populates='temperatures')
