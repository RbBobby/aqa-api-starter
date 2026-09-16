import pytest

from api.client import ApiClient


@pytest.fixture(scope="session")
def api_client():
    client = ApiClient()
    yield client
    client.close()
