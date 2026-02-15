from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject
from app.schemas import CharityProjectUpdate


async def update_with_investment_check(
    project: CharityProject,
    project_update: CharityProjectUpdate,
    session: AsyncSession
) -> CharityProject:
    """Обновление проекта с проверкой инвестиций."""
    update_data = project_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if hasattr(project, field):
            setattr(project, field, value)

    if (
        'full_amount' in update_data
        and project.invested_amount >= project.full_amount
    ):
        project.fully_invested = True
        project.close_date = datetime.now()

    session.add(project)
    await session.commit()
    await session.refresh(project)

    return project
