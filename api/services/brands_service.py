"""
Brands API (сценарии 3–4 на automationexercise.com/api_list).

  GET /brandsList — список брендов
  PUT /brandsList — метод не поддерживается → responseCode 405

TODO (практика ученика): напишите тесты по образцу
tests/api/test_products_list.py — GET 200 и PUT 405 в body.response_code.
Сервис уже готов, отдельный тест-файл пока специально не добавлен.
"""

from api.client.api_client import ApiClient, ApiResponse


class BrandsService:
    """API Object для /brandsList."""

    BRANDS_LIST = "/brandsList"

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def get_brands(self) -> ApiResponse:
        """API 3 — список брендов."""
        return self._client.get(self.BRANDS_LIST)

    def put_brands(self) -> ApiResponse:
        """API 4 — PUT запрещён (ожидайте 405 в теле ответа)."""
        return self._client.put(self.BRANDS_LIST)
