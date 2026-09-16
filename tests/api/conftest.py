"""
Fixtures = dependency injection для API-тестов.

Цепочка:

  settings (session)
      └── api_client (session)
              ├── products_service
              └── brands_service

Тест получает готовый сервис аргументом функции — сам клиент не создаёт.
"""

import pytest

from api.client.api_client import ApiClient
from api.config.settings import Settings, get_settings
from api.services.brands_service import BrandsService
from api.services.products_service import ProductsService


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Загрузить .env один раз на сессию pytest."""
    return get_settings()


@pytest.fixture(scope="session")
def api_client(settings: Settings) -> ApiClient:
    """Общая HTTP-сессия; закрывается после всех тестов."""
    client = ApiClient(base_url=settings.api_base_url, timeout=settings.api_timeout)
    yield client
    client.close()


@pytest.fixture
def products_service(api_client: ApiClient) -> ProductsService:
    return ProductsService(api_client)


@pytest.fixture
def brands_service(api_client: ApiClient) -> BrandsService:
    # Нужна, когда допишете tests/api/test_brands_list.py
    return BrandsService(api_client)
