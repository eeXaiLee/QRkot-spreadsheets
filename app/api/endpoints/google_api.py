from typing import Annotated

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.models import User
from app.services.google_api import (
    create_spreadsheets,
    get_projects_by_completion_rate,
    set_user_permissions,
    update_spreadsheets_value,
)

router = APIRouter()

SessionDependency = Annotated[AsyncSession, Depends(get_async_session)]
GoogleServiceDependency = Annotated[Aiogoogle, Depends(get_service)]


@router.post(
    '/',
    summary='Generate Google Sheets Report',
    description='Создание Google таблицы с отчётом по закрытым проектам.'
)
async def generate_report(
    session: SessionDependency,
    wrapper_services: GoogleServiceDependency,
    user: Annotated[User, Depends(current_superuser)]
):
    projects = await get_projects_by_completion_rate(session)
    spreadsheet_id = await create_spreadsheets(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    await update_spreadsheets_value(spreadsheet_id, projects, wrapper_services)

    return {
        'message': 'Отчёт успешно создан',
        'spreadsheet_id': spreadsheet_id
    }
