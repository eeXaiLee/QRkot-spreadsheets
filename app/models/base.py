from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class InvestmentBase(Base):

    __abstract__ = True

    __table_args__ = (
        CheckConstraint(
            'full_amount > 0',
            name='check_full_amount_positive'
        ),
        CheckConstraint(
            'invested_amount >= 0',
            name='check_invested_amount_non_negative'
        ),
        CheckConstraint(
            'invested_amount <= full_amount',
            name='check_invested_not_exceed_full'
        ),
    )

    full_amount: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    invested_amount: Mapped[int] = mapped_column(
        Integer, default=0
    )
    fully_invested: Mapped[bool] = mapped_column(
        Boolean, default=False
    )
    create_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )
    close_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=True
    )
