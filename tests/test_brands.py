def test_get_brands(api_client):
    response = api_client.get("/brandsList")

    assert response.status_code == 200
    assert response.reason == "OK"

    data = response.json()
    brands = data["brands"]

    assert isinstance(brands, list)
    assert len(brands) > 33

    brand_ids = []

    for brand in brands:
        # Проверяем структуру и типы данных
        assert isinstance(brand, dict)
        assert "id" in brand
        assert brand["id"] > 0
        assert isinstance(brand["brand"], str)

        # Проверяем, что название не пустое и не состоит из пробелов
        assert brand["brand"].strip() != ""

        brand_ids.append(brand["id"])

    # Проверяем отсутствие повторяющихся id
    assert len(brand_ids) == len(set(brand_ids))
