from datetime import datetime
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.containers import Container
from app.core.db import get_async_session
from app.models.base import InvestmentBase
from app.repositories import CharityProjectRepository, DonationRepository

SessionDependency = Annotated[AsyncSession, Depends(get_async_session)]


def _close_fully_invested_object(obj: InvestmentBase) -> bool:
    """Закрытие объекта, если он полностью профинансирован."""
    if obj.invested_amount >= obj.full_amount:
        obj.fully_invested = True
        obj.close_date = datetime.now()
        return True
    return False


def _calculate_remaining_amount(obj: InvestmentBase) -> int:
    """Возвращает оставшуюся сумму для инвестирования."""
    return obj.full_amount - obj.invested_amount


def _add_investment(obj: InvestmentBase, amount: int) -> None:
    """Добавить инвестированную сумму в объект."""
    obj.invested_amount += amount


def _update_index_if_closed(obj: InvestmentBase, index: int) -> int:
    """Вернуть увеличенный индекс, если объект закрыт."""
    if _close_fully_invested_object(obj):
        return index + 1
    return index


@inject
async def distribute_investments(
    session: AsyncSession,
    charity_project_repository: Annotated[
        CharityProjectRepository,
        Depends(Provide[Container.charity_project_repository])
    ],
    donation_repository: Annotated[
        DonationRepository,
        Depends(Provide[Container.donation_repository])
    ]
) -> None:
    """Распределить средства из пожертвований по проектам."""
    open_projects = (
        await charity_project_repository.get_open_sorted_by_created(session)
    )
    open_donations = (
        await donation_repository.get_open_sorted_by_created(session)
    )

    if not open_projects or not open_donations:
        return

    project_index = 0
    donation_index = 0

    while (
        project_index < len(open_projects)
        and donation_index < len(open_donations)
    ):
        project = open_projects[project_index]
        donation = open_donations[donation_index]

        need_amount = _calculate_remaining_amount(project)
        available_amount = _calculate_remaining_amount(donation)

        transfer_amount = min(need_amount, available_amount)

        _add_investment(project, transfer_amount)
        _add_investment(donation, transfer_amount)

        project_index = _update_index_if_closed(project, project_index)
        donation_index = _update_index_if_closed(donation, donation_index)

    await session.commit()
