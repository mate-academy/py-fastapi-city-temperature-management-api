class DatabaseError(Exception):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args)
        if "message" in kwargs:
            self.message = kwargs["message"]
            return
        try:
            split = str(args[0]).split()
            field = split[-1].split(".")[-1]
            self.message = {
                field: "Invalid field value"
            }
        except (IndexError, AttributeError):
            self.message = {"msg": "One or more fields values are invalid"}
