def test_get_brands(api_client):
    response = api_client.get("/brandsList")

    assert response.status_code == 200
    assert response.reason == "OK"

    data = response.json()

    assert len(data["brands"]) > 33