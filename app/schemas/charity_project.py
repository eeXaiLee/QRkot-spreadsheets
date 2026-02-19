from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, field_validator


class CharityProjectBase(BaseModel):

    name: str | None = Field(None, min_length=5, max_length=100)
    description: str | None = Field(None, min_length=10)
    full_amount: PositiveInt | None = None

    model_config = ConfigDict(extra='forbid')


class CharityProjectCreate(CharityProjectBase):
    """Создание проекта."""

    name: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10)
    full_amount: PositiveInt = Field(...)


class CharityProjectDB(CharityProjectCreate):
    """Проект из БД."""

    id: int
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime
    close_date: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class CharityProjectUpdate(CharityProjectBase):
    """Обновление проекта"""

    @field_validator('name')
    def name_cannot_be_null(cls, value: str | None) -> str | None:
        """Имя проекта обязательно при обновлении."""
        if value is None or value == '':
            raise ValueError('Имя проекта не может быть пустым!')
        return value
