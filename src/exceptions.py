class CityBaseException(Exception):
    pass


class TemperatureBaseException(Exception):
    pass


class CityNotFoundError(CityBaseException):
    def __init__(self, message: str = "City not found"):
        self.message = message
        super().__init__(message)


class KeyNotConfigure(TemperatureBaseException):
    def __init__(
        self,
        message: str = "OpenWeather API key not configured",
    ) -> None:
        self.message = message
        super().__init__(message)
