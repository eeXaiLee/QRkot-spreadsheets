from dependency_injector import containers, providers
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from app.core.db import AsyncSessionLocal, get_async_session
from app.core.user import UserManager
from app.models import CharityProject, Donation, User
from app.repositories import CharityProjectRepository, DonationRepository


class Container(containers.DeclarativeContainer):
    """DI контейнер."""

    config = providers.Configuration()

    db_session_factory = providers.Factory(
        AsyncSessionLocal
    )

    db_session = providers.Resource(
        get_async_session
    )

    charity_project_repository = providers.Singleton(
        CharityProjectRepository,
        model=CharityProject
    )

    donation_repository = providers.Singleton(
        DonationRepository,
        model=Donation
    )

    user_db = providers.Singleton(
        SQLAlchemyUserDatabase,
        session=db_session,
        user_table=User
    )

    user_manager = providers.Singleton(
        UserManager,
        user_db=user_db
    )
