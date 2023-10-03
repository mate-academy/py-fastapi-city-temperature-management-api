import os

from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend

cookie_transport = CookieTransport(cookie_name="city_temperature_site", cookie_max_age=3600)


SECRET_JWT = os.getenv('SECRET_JWT')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_JWT, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
