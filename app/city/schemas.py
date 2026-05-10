from pydantic import BaseModel


class CityBase(BaseModel):
	name: str
	additional_info: str | None = None


class CityCreate(CityBase):
	...


class CityUpdate(CityBase):
	...


class CityList(CityBase):
	id: int
