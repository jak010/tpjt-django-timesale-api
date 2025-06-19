from abc import abstractmethod


class IProductService:

    @abstractmethod
    def create_product(self, name: str, price: int, description: str):
        """ 상품 생성하기

        Args:
            name (str): 상품명
            price (int): 상품가격
            description (str): 상품설명

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
