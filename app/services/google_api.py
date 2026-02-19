from datetime import datetime
from typing import Sequence

from aiogoogle import Aiogoogle
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models import CharityProject
from app.repositories import CharityProjectRepository

FORMAT = '%Y/%m/%d %H:%M:%S'


async def get_projects_by_completion_rate(
    session: AsyncSession
) -> Sequence[CharityProject]:
    """Возвращает закрытые проекты, отсортированные по скорости закрытия."""
    repository = CharityProjectRepository(CharityProject)
    return await repository.get_closed_projects_sorted_by_completion_rate(
        session
    )


async def create_spreadsheets(wrapper_services: Aiogoogle) -> str:
    """Создание новой Google таблицы."""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')

    spreadsheet_body = {
        'properties': {
            'title': f'Отчет от {now_date_time}',
            'locale': 'ru_RU'
        },
        'sheets': [{
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'Лист1',
                'gridProperties': {
                    'rowCount': 100,
                    'columnCount': 11
                }
            }
        }]
    }

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )

    return response['spreadsheetId']


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_services: Aiogoogle
) -> None:
    """Выдача прав на редактирование личному аккаунту."""
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }

    service = await wrapper_services.discover('drive', 'v3')

    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        )
    )


async def update_spreadsheets_value(
    spreadsheet_id: str,
    projects: Sequence[CharityProject],
    wrapper_services: Aiogoogle
) -> None:
    """Заполнение Google таблицы данными о закрытых проектах."""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')

    table_values = [
        ['Отчет от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]

    for project in projects:
        collection_time = str(project.close_date - project.create_date)

        new_row = [
            project.name,
            collection_time,
            project.description
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:C30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
