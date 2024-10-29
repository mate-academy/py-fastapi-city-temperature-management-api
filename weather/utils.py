from datetime import datetime
import os
from typing import Callable
import json

from fastapi import HTTPException


def check_write_access():
    filepath = os.getcwd()

    if os.access(filepath, os.W_OK):
        print("Access granted")
    else:
        print("Denied")


def exception_handler(func: Callable) -> Callable:
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as error:
            check_write_access()
            with open("exception_log.txt", "a+") as file:
                data = {
                    "date": str(datetime.now()),
                    "message": str(error),
                }

                if hasattr(error, "status_code"):
                    data["status_code"] = error.status_code
                else:
                    data["status_code"] = 500

                if hasattr(error, "detail"):
                    data["detail"] = error.detail

                file.write(json.dumps(data) + "\n")
            raise error

    return wrapper
