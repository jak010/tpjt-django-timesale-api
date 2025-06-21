from __future__ import annotations

from typing import Optional, List, TYPE_CHECKING

from django.db import transaction

from apps.models.product import Product
from apps.services.interfaces import IProductService

if TYPE_CHECKING:
    from apps.views.v1.product_view import CreateProductRequestDto


class ProductService(IProductService):

    @transaction.atomic()
    def create_product(self, *, command: CreateProductRequestDto):
        """ 상품 생성하기 """

        new_product = Product.init_entity(
            name=command.validated_data["name"],
            price=command.validated_data["price"],
            description=command.validated_data["description"]
        )
        new_product.save()
        return new_product

    def get_product(self, product_id: int) -> Optional[Product]:
        """ 상품 조회 """

        product = Product.objects.filter(product_id=product_id)
        if product.exists():
            return product.first()

        raise Exception("Product Not Found")

    def get_all_products(self) -> List[Product]:
        """ 상품 목록조회 """
        return Product.objects.all()
