from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey

from database import Base, engine


class DBTemperature(Base):
    __tablename__ = "temperature"
    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("city.id"))
    date_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    temperature = Column(Float, nullable=False)


Base.metadata.create_all(bind=engine)
