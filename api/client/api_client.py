"""
HTTP-слой для Automation Exercise API.

Зачем отдельный клиент, а не requests.get() прямо в тесте:
  1. Один Session на весь прогон — cookies и keep-alive.
  2. Все URL собираются от base_url, сервисы знают только path.
  3. Тест работает с ApiResponse (status + typed .body), а не с сырым Response.

Особенность сайта: HTTP-статус часто 200 даже при ошибке.
Смотрите response.body.response_code, а не только status_code.
"""

import logging
from functools import cached_property
from typing import Any, Optional

import requests

from api.models.responses import ApiBody

logger = logging.getLogger(__name__)


class ApiResponse:
    """Обёртка над requests.Response — удобные свойства для assert в тестах."""

    def __init__(self, response: requests.Response) -> None:
        self._response = response

    @property
    def status_code(self) -> int:
        """HTTP status (на этом сайте обычно 200)."""
        return self._response.status_code

    @property
    def text(self) -> str:
        return self._response.text

    @property
    def json(self) -> Any:
        """Сырой JSON (dict/list). Для проверок лучше .body."""
        return self._response.json()

    @cached_property
    def body(self) -> ApiBody:
        """Типизированное тело: response_code, message, products, brands."""
        return ApiBody.from_dict(self.json)

    @property
    def ok(self) -> bool:
        return self._response.ok


class ApiClient:
    """
    Общий HTTP-клиент для всех сервисов.

    Создаётся один раз на сессию pytest (см. tests/api/conftest.py).
    Сервисы вызывают get/post/put/delete, а не request() напрямую.
    """

    def __init__(self, base_url: str, timeout: int = 30) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()

    def close(self) -> None:
        """Закрыть TCP-соединения (teardown fixture)."""
        self._session.close()

    def request(
        self,
        method: str,
        path: str,
        *,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        **kwargs: Any,
    ) -> ApiResponse:
        """
        Низкоуровневый запрос. Аргументы после * — только keyword,
        чтобы не перепутать data и params позиционно.
        """
        url = f"{self.base_url}{path}"
        kwargs.setdefault("timeout", self.timeout)
        response = self._session.request(method, url, data=data, params=params, **kwargs)
        logger.debug("%s %s -> %s", method.upper(), url, response.status_code)
        return ApiResponse(response)

    def get(self, path: str, **kwargs: Any) -> ApiResponse:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> ApiResponse:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> ApiResponse:
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> ApiResponse:
        return self.request("DELETE", path, **kwargs)
