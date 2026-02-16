from typing import Sequence

from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject
from app.repositories.base import RepositoryBase


class GoogleReportRepository(RepositoryBase):
    """Репозиторий для формирования отчётов."""

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
