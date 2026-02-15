from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists,
    check_full_amount_not_less_than_invested,
    check_name_duplicate,
    check_project_has_no_investments,
    check_project_not_closed,
)
from app.containers import Container
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.models import User
from app.repositories import CharityProjectRepository
from app.schemas import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.charity_project import update_with_investment_check
from app.services.investment import distribute_investments

router = APIRouter()

SessionDependency = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
    summary='Get All Charity Projects',
    description='Показать список всех целевых проектов.',
)
@inject
async def get_all_charity_projects(
    session: SessionDependency,
    charity_project_repository: Annotated[
        CharityProjectRepository,
        Depends(Provide[Container.charity_project_repository])
    ]
):
    return await charity_project_repository.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    summary='Create Charity Project',
    description='Создать целевой проект.'
)
@inject
async def create_charity_project(
    project: CharityProjectCreate,
    session: SessionDependency,
    charity_project_repository: Annotated[
        CharityProjectRepository,
        Depends(Provide[Container.charity_project_repository])
    ],
    user: Annotated[User, Depends(current_superuser)]
):
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_repository.create(project, session)
    await distribute_investments(session)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    summary='Update Charity Project',
    description='Редактировать целевой проект.'
)
@inject
async def update_charity_project(
    project_id: int,
    project_update: CharityProjectUpdate,
    session: SessionDependency,
    user: Annotated[User, Depends(current_superuser)]
):
    project = await check_charity_project_exists(project_id, session)
    await check_project_not_closed(project)

    if project_update.name is not None:
        await check_name_duplicate(project_update.name, session)

    await check_full_amount_not_less_than_invested(
        project, project_update.full_amount
    )

    project = await update_with_investment_check(
        project, project_update, session
    )

    await distribute_investments(session)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    summary='Delete Charity Project',
    description='Удалить целевой проект.',
)
@inject
async def delete_charity_project(
    project_id: int,
    session: SessionDependency,
    charity_project_repository: Annotated[
        CharityProjectRepository,
        Depends(Provide[Container.charity_project_repository])
    ],
    user: Annotated[User, Depends(current_superuser)]
):
    project = await check_charity_project_exists(project_id, session)
    await check_project_has_no_investments(project)
    project = await charity_project_repository.remove(project, session)
    return project
