class CityAlreadyExistsException(Exception):
    def __init__(self, city_name: str):
        self.city_name = city_name
        super().__init__(f"City with name '{city_name}' already exists.")
