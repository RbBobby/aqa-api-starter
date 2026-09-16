"""
Типизированные модели JSON-ответов Automation Exercise.

Сайт отдаёт camelCase: responseCode, products, brands.
ApiBody.from_dict() — единственная точка парсинга; её вызывает ApiResponse.body.
"""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Product:
    """Один товар из GET /productsList."""

    id: int
    name: str
    price: str
    brand: str
    category: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Product":
        return cls(
            id=data["id"],
            name=data["name"],
            price=data["price"],
            brand=data["brand"],
            category=data["category"],
        )


@dataclass
class Brand:
    """Одна запись из GET /brandsList."""

    brand: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Brand":
        return cls(brand=data["brand"])


@dataclass
class ApiBody:
    """
    Верхний уровень JSON любого ответа этого API.

    response_code — поле JSON "responseCode" (бизнес-результат, не HTTP-код).
    raw — исходный dict, если понадобится поле, которого ещё нет в модели.
    """

    response_code: int
    message: Optional[str] = None
    products: list[Product] = field(default_factory=list)
    brands: list[Brand] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ApiBody":
        products = [Product.from_dict(item) for item in data.get("products", [])]
        brands = [Brand.from_dict(item) for item in data.get("brands", [])]
        return cls(
            response_code=data["responseCode"],
            message=data.get("message"),
            products=products,
            brands=brands,
            raw=data,
        )
