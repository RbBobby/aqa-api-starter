def test_get_products(api_client):
    response = api_client.get("/productsList")
    body = response.json()

    assert response.status_code == 200
    assert body["responseCode"] == 200
    assert body["products"]


def test_post_products_not_supported(api_client):
    response = api_client.post("/productsList")
    body = response.json()

    # HTTP 200, ошибка в JSON — особенность этого API
    assert response.status_code == 200
    assert body["responseCode"] == 405
    assert body["message"] == "This request method is not supported."
