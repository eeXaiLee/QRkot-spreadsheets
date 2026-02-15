from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class DonationBase(BaseModel):

    full_amount: PositiveInt = Field(...)
    comment: str | None = Field(None)


class DonationCreate(DonationBase):
    """Создание пожертвования."""


class DonationDB(DonationCreate):
    """Пожертвование из БД."""

    id: int
    create_date: datetime

    model_config = ConfigDict(from_attributes=True)


class DonationFullInfoDB(DonationDB):
    """Полная схема пожертвования с инвестиционной информацией."""

    invested_amount: int = Field(0)
    fully_invested: bool = Field(False)
    close_date: datetime | None = Field(None)
    user_id: int = Field(...)
