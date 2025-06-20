import pytest
from django.test import override_settings  # noqa

from apps.models import Product
from src.apps.services.interfaces.i_product_service import IProductService
from src.apps.services.v1.product_service import ProductService


@pytest.mark.django_db
class TestProductServiceV1:
    """IProductService 인터페이스 테스트 케이스"""

    def setup_class(self):
        self.product_service: IProductService = ProductService()

    # =============================================================================
    # create_product 메서드 테스트 케이스
    # =============================================================================

    # @override_settings(DEBUG=True)
    def test_create_product_success(self):
        """상품 생성 테스트 - 성공"""

        new_product = self.product_service.create_product(
            name="테스트 상품",
            price=1000,
            description="테스트 상품 1"
        )

        assert new_product.name == "테스트 상품"
        assert new_product.price == 1000
        assert new_product.description, "테스트 상품 세로 고급한 상품이다"

    def test_create_product_missing_name(self):
        """상품명 누락 시 예외 처리 테스트"""

        with pytest.raises(Exception, match="Product Name is Empty"):
            self.product_service.create_product(
                name=None,
                price=1000,
                description="테스트 상품 1"
            )

    def test_create_product_missing_price(self):
        """가격 누락 시 예외 처리 테스트"""

        with pytest.raises(Exception, match="Product Price is Empty"):
            self.product_service.create_product(
                name="test price",
                price=None,
                description="테스트 상품 1"
            )

    def test_create_product_missing_description(self):
        """상품설명 누락 시 예외 처리 테스트"""
        with pytest.raises(Exception, match="Product Description is Empty"):
            self.product_service.create_product(
                name="test price",
                price=1000,
                description=None
            )

    def test_create_product_invalid_price_type(self):
        """잘못된 가격 타입 전달 시 테스트"""

        with pytest.raises(ValueError):
            self.product_service.create_product(
                name="test price",
                price="test",
                description="test description"
            )

    def test_create_product_empty_name(self):
        """빈 상품명 전달 시 테스트"""
        with pytest.raises(Exception, match="Product Name is Empty"):
            self.product_service.create_product(
                name="",
                price=1000,
                description="test description"
            )

    def test_create_product_negative_price(self):
        """음수 가격 전달 시 테스트"""
        with pytest.raises(Exception, match="Product Price is Negative"):
            self.product_service.create_product(
                name="test price",
                price=-1000,
                description="test description"
            )

    # =============================================================================
    # get_product 메서드 테스트 케이스
    # =============================================================================

    def test_get_product_existing_id(self):
        """존재하는 상품 ID로 조회 성공 테스트"""

        product = self.product_service.create_product(
            name="test price",
            price=1000,
            description="test description"
        )

        product = self.product_service.get_product(product_id=product.product_id)

        assert product.name == "test price"

    def test_get_product_non_existing_id(self):
        """존재하지 않는 상품 ID로 조회 시 예외 처리 테스트"""

        with pytest.raises(Exception, match="Product Not Found"):
            self.product_service.get_product(product_id=99999)

    # =============================================================================
    # get_all_products 메서드 테스트 케이스
    # =============================================================================

    def test_get_all_products_with_data(self):
        """상품이 존재할 때 전체 목록 조회 테스트"""
        # TODO: 상품 데이터가 존재할 때 목록 조회 성공 검증

        for _ in range(5):
            self.product_service.create_product(
                name="test price",
                price=_,
                description="test description"
            )

        products = self.product_service.get_all_products()

        assert len(products) == 5

        for product in products:
            assert isinstance(product, Product)

    def test_get_all_products_empty(self):
        """상품이 존재하지 않을 때 빈 목록 반환 테스트"""

        products = self.product_service.get_all_products()

        assert len(products) == 0
