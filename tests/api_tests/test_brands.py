import allure
import pytest

from api.services.brands_service import BrandsService

@allure.epic("API")
@allure.feature("Brands")
@allure.story("GET /brandsList")
@allure.title("Список брендов возвращается и валиден")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "brands")
@pytest.mark.api
def test_get_brands(api_client):
    with allure.step("Запросить список брендов"):
        brands = BrandsService(api_client).get_brands()


    with allure.step("Проверить структуру, типы и уникальность брендов"):
        brand_ids = []

        for brand in brands:
            assert isinstance(brand, dict)
            assert "id" in brand
            assert "brand" in brand
            assert type(brand["id"]) is int
            assert brand["id"] > 0
            assert isinstance(brand["brand"], str)
            assert brand["brand"].strip() != ""
            brand_ids.append(brand["id"])

        assert len(brand_ids) == len(set(brand_ids))
