"""
Products API (сценарии 1–2 на automationexercise.com/api_list).

  GET  /productsList — каталог товаров
  POST /productsList — метод не поддерживается → responseCode 405

Паттерн Service Object: один эндпоинт — один класс.
Тест вызывает get_products(), а не клиент.get("/productsList").
"""

from api.client.api_client import ApiClient, ApiResponse


class ProductsService:
    """API Object для /productsList."""

    PRODUCTS_LIST = "/productsList"

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def get_products(self) -> ApiResponse:
        """API 1 — полный список товаров."""
        return self._client.get(self.PRODUCTS_LIST)

    def post_products(self) -> ApiResponse:
        """API 2 — POST запрещён (ожидайте 405 в теле ответа)."""
        return self._client.post(self.PRODUCTS_LIST)
