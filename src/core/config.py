"""
Файл для загрузки и валидации всех настроек приложения.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PositiveInt


class AppSettings(BaseSettings):
    """Главный класс настроек приложения."""

    MAX_PRO_CON_LENGTH: PositiveInt = Field(
        default=200, description="Макс. длина элемента pros/cons"
    )
    DEFAULT_START_YEAR_DEVICE: PositiveInt = Field(
        default=1990, description="Год, начиная с которого валидируются устройства"
    )
    DEFAULT_IMAGE_DEVICE: str = Field(
        default="images/", description="Путь к картинке по умолчанию"
    )


settings = AppSettings()
