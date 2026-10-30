from api.services.base_service import BaseService

class BrandsService(BaseService):
    def get_brands(self) -> list[dict]:
        response = self.client.get("/brandsList")
        self.check_response(response, 201)
        return response.json()["brands"]