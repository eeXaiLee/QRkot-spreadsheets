from typing import Sequence

from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject
from app.models.charity_project import CharityProject
from app.repositories.base_investment import BaseInvestmentRepository


class CharityProjectRepository(BaseInvestmentRepository):
    """Репозиторий для проектов."""

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession
    ) -> int | None:
        """Поиск ID проекта по имени."""
        result = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = result.scalars().first()
        return db_project_id

    async def get_closed_projects_sorted_by_completion_rate(
        self,
        session: AsyncSession
    ) -> Sequence[CharityProject]:
        """Получение проектов, отсортированных по скорости закрытия."""
        completion_time = (
            extract('epoch', CharityProject.close_date) -
            extract('epoch', CharityProject.create_date)
        )

        stmt = (
            select(CharityProject)
            .where(CharityProject.fully_invested.is_(True))
            .order_by(completion_time)
        )

        result = await session.execute(stmt)
        return result.scalars().all()
