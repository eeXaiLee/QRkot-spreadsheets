from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Просмотр пользователя."""


class UserCreate(schemas.BaseUserCreate):
    """Создание пользователя."""


class UserUpdate(schemas.BaseUserUpdate):
    """Обновление пользователя."""
