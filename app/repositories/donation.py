from typing import Any, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base_investment import BaseInvestmentRepository


class DonationRepository(BaseInvestmentRepository):
    """Репозиторий для пожертвований."""

    async def get_by_user(
        self,
        session: AsyncSession,
        user_id: int
    ) -> Sequence[Any]:
        """Получить пожертвования конкретного пользователя."""
        stmt = select(self.model).where(self.model.user_id == user_id)
        result = await session.execute(stmt)
        return result.scalars().all()
