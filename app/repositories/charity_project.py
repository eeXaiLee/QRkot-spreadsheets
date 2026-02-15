from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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
