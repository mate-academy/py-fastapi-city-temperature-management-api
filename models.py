from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from city.models import City
from temperature.models import Temperature
