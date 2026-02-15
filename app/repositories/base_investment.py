from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import RepositoryBase


class BaseInvestmentRepository(RepositoryBase):
    """Базовый репозиторий для инвестиционных моделей."""

    async def get_open_sorted_by_created(
        self,
        session: AsyncSession
    ) -> Sequence[Any]:
        stmt = (
            select(self.model)
            .where(self.model.fully_invested.is_(False))
            .order_by(self.model.create_date)
        )
        result = await session.execute(stmt)
        return result.scalars().all()
