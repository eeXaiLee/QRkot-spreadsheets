from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Конфигурация приложения."""

    app_title: str = 'Благотворительный фонд поддержки котиков QRKot'
    description: str = 'Сервис для поддержки котиков'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret_key: str = 'secret_key'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='QRKOT_',
        case_sensitive=True,
        extra='allow'
    )


settings = Settings()
