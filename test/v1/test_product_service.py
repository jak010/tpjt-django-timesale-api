import pytest
from django.test import override_settings  # noqa

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
        # TODO: 존재하는 product_id로 조회 성공 검증
        assert False

    def test_get_product_non_existing_id(self):
        """존재하지 않는 상품 ID로 조회 시 예외 처리 테스트"""
        # TODO: 존재하지 않는 product_id로 조회 시 예외 발생 검증
        assert False

    def test_get_product_invalid_id_type_string(self):
        """문자열 상품 ID 전달 시 테스트"""
        # TODO: 문자열 product_id 전달 시 예외 발생 검증
        assert False

    def test_get_product_invalid_id_type_none(self):
        """None 상품 ID 전달 시 테스트"""
        # TODO: None product_id 전달 시 예외 발생 검증
        assert False

    def test_get_product_negative_id(self):
        """음수 상품 ID 전달 시 테스트"""
        # TODO: 음수 product_id 전달 시 예외 발생 검증
        assert False

    def test_get_product_zero_id(self):
        """0 값 상품 ID 전달 시 테스트"""
        # TODO: 0 값 product_id 전달 시 예외 발생 검증
        assert False

    # =============================================================================
    # get_all_products 메서드 테스트 케이스
    # =============================================================================

    def test_get_all_products_with_data(self):
        """상품이 존재할 때 전체 목록 조회 테스트"""
        # TODO: 상품 데이터가 존재할 때 목록 조회 성공 검증
        assert False

    def test_get_all_products_empty(self):
        """상품이 존재하지 않을 때 빈 목록 반환 테스트"""
        # TODO: 상품이 없을 때 빈 목록 반환 검증
        assert False

    def test_get_all_products_large_dataset(self):
        """대량의 상품 데이터 조회 성능 테스트"""
        # TODO: 대량 데이터 조회 시 성능 및 정확성 검증
        assert False

    # =============================================================================
    # 인터페이스 구현 테스트 케이스
    # =============================================================================

    def test_abstract_methods_not_implemented_error(self):
        """추상 메서드가 구현되지 않은 경우 NotImplementedError 발생 테스트"""
        # TODO: 인터페이스 직접 인스턴스화 시 NotImplementedError 검증
        assert False

    def test_interface_inheritance_verification(self):
        """인터페이스 상속 및 구현 검증 테스트"""
        # TODO: 구현체가 올바르게 인터페이스를 상속했는지 검증
        assert False

    # =============================================================================
    # 통합 테스트 케이스
    # =============================================================================

    def test_create_and_get_product_integration(self):
        """상품 생성 후 조회 연동 테스트"""
        # TODO: 상품 생성 후 해당 상품 조회 성공 검증
        assert False

    def test_create_multiple_products_and_get_all(self):
        """여러 상품 생성 후 전체 목록 조회 테스트"""
        # TODO: 여러 상품 생성 후 전체 목록에서 모든 상품 확인
        assert False

    def test_product_creation_order_consistency(self):
        """상품 생성/조회 순서에 따른 일관성 테스트"""
        # TODO: 생성 순서와 조회 순서의 일관성 검증
        assert False

    def test_product_data_integrity(self):
        """상품 데이터 무결성 테스트"""
        # TODO: 생성한 상품 데이터와 조회한 상품 데이터의 일치성 검증
        assert False
