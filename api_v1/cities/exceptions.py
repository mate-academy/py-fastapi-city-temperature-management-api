CITY_NAME_CONFLICT_DETAIL = "City with this name already exists"


class CityNameConflict(Exception):
    def __init__(self, detail: str = CITY_NAME_CONFLICT_DETAIL) -> None:
        super().__init__(detail)
