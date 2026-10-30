import allure
from requests import Response

from api.client import ApiClient

class BaseService:
    def __init__(self, client: ApiClient):
        self.client = client

    @allure.step("Проверить ответ")
    def check_response(self, response: Response, expected_code: int):
        with allure.step("Проверить статус код"):
            assert response.status_code == expected_code, f"Ожидаемый статус {expected_code}, но получаемый статус {response.status_code}"

        with allure.step("Проверить валидность JSON"):
            try:
                response.json()
            except Exception as e:
                raise ValueError(f"Ответ не является JSON: {response.text}") from e
                
        return response
