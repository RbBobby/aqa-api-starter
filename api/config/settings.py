"""
Настройки из окружения (.env или переменные OS).

Скопируйте .env.example → .env. Для учебного минимума достаточно URL и таймаута.
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

DEFAULT_API_BASE_URL = "https://automationexercise.com/api"
DEFAULT_API_TIMEOUT = 30


@dataclass(frozen=True)
class Settings:
    """Неизменяемые настройки прогона API-тестов."""

    api_base_url: str
    api_timeout: int


def get_settings() -> Settings:
    return Settings(
        api_base_url=os.getenv("API_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/"),
        api_timeout=int(os.getenv("API_TIMEOUT", DEFAULT_API_TIMEOUT)),
    )
