from typing import Optional, List

from django.db import transaction

from src.apps.models.product import Product
from src.apps.services.interfaces import IProductService


class ProductService(IProductService):

    @transaction.atomic()
    def create_product(self, *, name: str, price: int, description: str):
        """ 상품 생성하기

        TODO
        - 25.06.19 : Argument Objects로 Refactoring
        """

        new_product = Product.init_entity(name=name, price=price, description=description)
        new_product.save()
        return new_product

    def get_product(self, product_id: int) -> Optional[Product]:
        product = Product.objects.filter(product_id=product_id)
        if product.exists():
            return product.first()

        raise Exception("Product Not Found")

    def get_all_products(self) -> List[Product]:
        return Product.objects.all()
