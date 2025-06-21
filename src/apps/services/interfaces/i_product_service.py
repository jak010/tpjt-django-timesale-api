from abc import abstractmethod

from apps.models.product import Product
from apps.views.request import CreateProductRequestDto


class IProductService:

    @abstractmethod
    def create_product(self, command: CreateProductRequestDto) -> Product:
        """ 상품 생성하기

        Args:
            command (CreateProductRequestDto):

        """
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_product(self, product_id: int):
        """ 상품 조회하기

        Args:
            product_id (int): 상품번호

        """
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_all_products(self):
        """ 상품 목록조회 """
        raise NotImplementedError("Method not implemented")
