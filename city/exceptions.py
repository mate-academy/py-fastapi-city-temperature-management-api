class CityAlreadyExistsError(Exception):
    """Raised when a city with the same name already exists."""

    def __init__(self, name: str) -> None:
        super().__init__(f"City '{name}' already exists")
        self.name = name
