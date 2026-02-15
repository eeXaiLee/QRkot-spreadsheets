from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import CommonMixin
from app.models.base import InvestmentBase


class CharityProject(CommonMixin, InvestmentBase):
    """Благотворительный проект."""

    name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )
    description: Mapped[str] = mapped_column(
        String, nullable=False
    )

    def __repr__(self):
        return f'Проект {self.name}'
