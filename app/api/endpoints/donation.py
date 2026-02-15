from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.containers import Container
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.models import User
from app.repositories import DonationRepository
from app.schemas import DonationCreate, DonationDB, DonationFullInfoDB
from app.services.investment import distribute_investments

router = APIRouter()

SessionDependency = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    response_model_exclude_none=True,
    summary='Get All Donations',
    description='Показать список всех пожертвований.',
)
@inject
async def get_all_donations(
    session: SessionDependency,
    donation_repository: Annotated[
        DonationRepository,
        Depends(Provide[Container.donation_repository])
    ],
    user: Annotated[User, Depends(current_superuser)]
):
    return await donation_repository.get_multi(session)


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    summary='Create Donation',
    description='Создать пожертвование.',
)
@inject
async def create_donation(
    donation: DonationCreate,
    session: SessionDependency,
    donation_repository: Annotated[
        DonationRepository,
        Depends(Provide[Container.donation_repository])
    ],
    user: Annotated[User, Depends(current_user)]
):
    new_donation = await donation_repository.create(donation, session, user)
    await distribute_investments(session)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    summary='Get User Donations',
    description='Показать список пожертвований пользователя.',
)
@inject
async def get_user_donations(
    session: SessionDependency,
    donation_repository: Annotated[
        DonationRepository,
        Depends(Provide[Container.donation_repository])
    ],
    user: Annotated[User, Depends(current_user)]
):
    return await donation_repository.get_by_user(session, user.id)
