from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import CommonMixin
from app.models.base import InvestmentBase


class Donation(CommonMixin, InvestmentBase):
    """Пожертвования."""

    comment: Mapped[str] = mapped_column(
        String, nullable=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id', name='fk_donation_user_id_user'),
        nullable=False
    )

    def __repr__(self):
        return f'Пожертвование {self.id}'
