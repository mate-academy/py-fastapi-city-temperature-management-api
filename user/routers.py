from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers

from user.auth import auth_backend
from user.crud import get_user_manager
from user.models import User

router = APIRouter()

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()


@router.get("/protected-route/")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"


@router.get("/unprotected-route/")
def protected_route():
    return f"Hello, anonim"
