import logging
from http import HTTPStatus
from typing import AsyncGenerator

from fastapi import Depends, HTTPException, Request
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models import User
from app.schemas import UserCreate

logger = logging.getLogger(__name__)

bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret_key, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """Менеджер пользователей."""

    async def validate_password(
        self,
        password: str,
        user: UserCreate | User
    ) -> None:
        if len(password) < 3:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail={
                    'code': 'REGISTER_INVALID_PASSWORD',
                    'reason': 'Пароль должен содержать не менее 3 символов'
                }
            )
        if user.email in password:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail={
                    'code': 'REGISTER_INVALID_PASSWORD',
                    'reason': 'Пароль не может содержать ваш email'
                }
            )

    async def on_after_register(
        self, user: User, request: Request | None = None
    ):
        logger.info('Пользователь %s зарегистрирован.', user.email)


async def get_user_db(
    session: AsyncSession = Depends(get_async_session)
) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db)
) -> AsyncGenerator[UserManager, None]:
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
