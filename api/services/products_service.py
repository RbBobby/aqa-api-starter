from api.services.base_service import BaseService

class ProductsService(BaseService):
    def get_products(self) -> list[dict]:
        response = self.client.get("/productsList")
        self.check_response(response, 200)
        return response.json()["products"]