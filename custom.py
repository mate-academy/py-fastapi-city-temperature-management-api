from sqlalchemy import text
from sqlalchemy.orm import mapped_column

from typing import Annotated
import datetime

intpk = Annotated[int, mapped_column(primary_key=True, index=True)]
date_time = Annotated[
    datetime.datetime,
    mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    ]