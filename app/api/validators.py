from http import HTTPStatus
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.containers import Container
from app.core.db import get_async_session
from app.models.charity_project import CharityProject
from app.repositories.charity_project import CharityProjectRepository

SessionDependency = Annotated[AsyncSession, Depends(get_async_session)]


@inject
async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
    charity_project_repository: Annotated[
        CharityProjectRepository,
        Depends(Provide[Container.charity_project_repository])
    ]
) -> None:
    """Имя проекта должно быть уникальным."""
    project_id = await charity_project_repository.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


@inject
async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
    charity_project_repository: Annotated[
        CharityProjectRepository,
        Depends(Provide[Container.charity_project_repository])
    ]
) -> CharityProject:
    """Проект с указанным ID должен существовать в базе данных."""
    project = await charity_project_repository.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!',
        )
    return project


async def check_project_not_closed(
    project: CharityProject,
) -> None:
    """Закрытый проект нельзя редактировать."""
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_full_amount_not_less_than_invested(
    project: CharityProject,
    full_amount: int | None
) -> None:
    """Новая требуемая сумма не может быть меньше уже инвестированной."""
    if full_amount is not None and full_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                'Нельзя установить значение full_amount '
                'меньше уже вложенной суммы.'
            )
        )


async def check_project_has_no_investments(
    project: CharityProject
) -> None:
    """Проект с инвестированными средствами не может быть удален."""
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
