from typing import Annotated

from fastapi import Depends


async def common_parameters_with_id(
        city_id: int,
):
    return city_id

CommonParametersWithId = Annotated[int, Depends(common_parameters_with_id)]
