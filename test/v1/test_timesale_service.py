import datetime
from datetime import datetime, timedelta

import pytest

from apps.dto.timsale_dto import TimeSaleCreateRequestDto, TimeSalePurchaseRequestDto
from apps.models import Product, TimeSale, TimeSaleOrder
from apps.services.interfaces.i_timesale_service import ITimeSaleService
from apps.services.v1.timesale_service import TimeSaleService
from django.test import override_settings


@pytest.mark.django_db
class TestTimeSaleService:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.sut: ITimeSaleService = TimeSaleService()

    # -------------------------------
    # create_timesale()
    # -------------------------------

    def test_create_timesale_success(self):
        """타임세일 생성이 정상적으로 수행되는 경우"""

        new_product = Product.init_entity(
            name="Test Product",
            price=10000,
            description="Test Product Description"
        )
        new_product.save()

        new_timesale = self.sut.create_timesale(
            product_id=new_product.product_id,
            quantity=10,
            discount_price=5000,
            start_at=datetime.now(),
            end_at=datetime.now() + timedelta(days=1)

        )

        assert isinstance(new_timesale, TimeSale)
        assert new_timesale.product.product_id == new_product.product_id
        assert new_timesale.quantity == 10
        assert new_timesale.remaining_quantity == 10
        assert new_timesale.discount_price == 5000

    def test_create_timesale_fail_due_to_invalid_time(self):
        """시작 시간이 종료 시간보다 늦은 경우 예외가 발생하는지를 테스트합니다."""

        new_product = Product.init_entity(
            name="Test Product",
            price=10000,
            description="Test Product Description"
        )
        new_product.save()

        with pytest.raises(Exception):
            self.sut.create_timesale(
                product_id=new_product.product_id,
                quantity=10,
                discount_price=5000,
                start_at=datetime.now() + timedelta(days=1),
                end_at=datetime.now() - timedelta(days=1)
            )

    def test_create_timesale_with_not_exit_product(self):
        """ 존재하지 않은 상품으로 타임세일 생성 시 예외가 발생하는지 테스트 """
        with pytest.raises(Exception):
            self.sut.create_timesale(
                product_id=102391239239,
                quantity=10,
                discount_price=5000,
                start_at=datetime.now() + timedelta(days=1),
                end_at=datetime.now() - timedelta(days=1)
            )

    # -------------------------------
    # get_timesale()
    # -------------------------------

    def test_get_timesale_success(self):
        """유효한 타임세일 ID에 대해 상세 정보를 정상적으로 조회할 수 있는지 테스트합니다."""

        new_product = Product.init_entity(
            name="Test Product",
            price=10000,
            description="Test Product Description"
        )
        new_product.save()

        new_timesale = self.sut.create_timesale(
            product_id=new_product.product_id,
            quantity=10,
            discount_price=5000,
            start_at=datetime.now(),
            end_at=datetime.now() + timedelta(days=1)
        )

        assert new_timesale == self.sut.get_timesale(new_timesale.timesale_id)

    def test_get_timesale_not_found(self):
        """존재하지 않는 타임세일 ID로 조회 시 예외가 발생하는지를 테스트합니다."""

        with pytest.raises(Exception):
            self.sut.get_timesale(9999999)

    # -------------------------------
    # get_ongoing_timesales()
    # -------------------------------

    @override_settings(DEBUG=True)
    def test_get_ongoing_timesales_success(self):
        """현재 진행 중인 타임세일이 정상적으로 필터링되고 페이지네이션되어 반환되는지를 테스트합니다."""

        new_product = Product.init_entity(
            name="Test Product",
            price=10000,
            description="Test Product Description"
        )
        new_product.save()

        new_timesale = TimeSale.init_entity(
            product=new_product,
            quantity=10,
            discount_price=5000,
            start_at=datetime.now(),
            end_at=datetime.now() + timedelta(days=1),
            status=TimeSale.Status.ACTIVE
        )
        new_timesale.save()

        ongoing_timesales = self.sut.get_ongoing_timesales(0, 10)

        assert len(ongoing_timesales) >= 1

        for ongoing_timesale in ongoing_timesales:
            assert isinstance(ongoing_timesale, TimeSale)

    def test_get_ongoing_timesales_empty(self):
        """조건에 해당하는 타임세일이 없을 때 빈 리스트를 반환하는지를 테스트합니다."""

        new_product = Product.init_entity(
            name="Test Product",
            price=10000,
            description="Test Product Description"
        )
        new_product.save()

        new_timesale = TimeSale.init_entity(
            product=new_product,
            quantity=10,
            discount_price=5000,
            start_at=datetime.now(),
            end_at=datetime.now() + timedelta(days=1),
            status=TimeSale.Status.ACTIVE
        )
        new_timesale.save()

        ongoing_timesales = self.sut.get_ongoing_timesales(1, 10)

        assert len(ongoing_timesales) == 0

    # -------------------------------
    # purchase_time_sale()
    # -------------------------------

    def test_purchase_timesale_success(self):
        """타임세일 구매 요청이 정상적으로 처리되고 주문 및 재고 차감이 이루어지는지를 테스트합니다."""

        # Arrange
        new_product = Product.init_entity(
            name="Test Product",
            price=10000,
            description="Test Product Description"
        )
        new_product.save()

        new_timesale = TimeSale.init_entity(
            product=new_product,
            quantity=100,
            discount_price=5000,
            start_at=datetime.now(),
            end_at=datetime.now() + timedelta(days=1),
            status=TimeSale.Status.ACTIVE
        )
        new_timesale.save()

        command = TimeSaleCreateRequestDto(
            data={
                "user_id": 1,
                "product_id": new_product.product_id,
                "quantity": 10,
                "discount_price": 1000,
                "start_at": datetime.now(),
                "end_at": datetime.now() + timedelta(days=1)
            }
        )

        # Act
        timesale = self.sut.purchase_time_sale(new_timesale.timesale_id, command)

        # Assert
        assert isinstance(timesale, TimeSale)
        assert timesale.timesale_id == new_timesale.timesale_id

        timesale_order = TimeSaleOrder.objects.filter(time_sale=timesale).first()
        assert isinstance(timesale_order, TimeSaleOrder)
        assert timesale_order.time_sale.timesale_id == new_timesale.timesale_id

    def test_purchase_timesale_out_of_stock(self):
        """재고가 부족한 상황에서 예외가 발생하는지를 테스트합니다."""

        # Arrange
        new_product = Product.init_entity(
            name="Test Product",
            price=10000,
            description="Test Product Description"
        )
        new_product.save()

        new_timesale = TimeSale.init_entity(
            product=new_product,
            quantity=10,
            discount_price=5000,
            start_at=datetime.now(),
            end_at=datetime.now() + timedelta(days=1),
            status=TimeSale.Status.ACTIVE
        )
        new_timesale.save()

        command = TimeSaleCreateRequestDto(
            data={
                "user_id": 1,
                "product_id": new_product.product_id,
                "quantity": 100,
                "discount_price": 1000,
                "start_at": datetime.now(),
                "end_at": datetime.now() + timedelta(days=1)
            }
        )

        # Act
        with pytest.raises(ValueError, match="Not enough quantity available"):
            self.sut.purchase_time_sale(new_timesale.timesale_id, command)

    def test_purchase_timesale_not_in_progress(self):
        """ 타임세일 기간이 아닌 경우 구매 실패하기 """

        # Arrange
        new_product = Product.init_entity(
            name="Test Product",
            price=10000,
            description="Test Product Description"
        )
        new_product.save()

        new_timesale = TimeSale.init_entity(
            product=new_product,
            quantity=10,
            discount_price=5000,
            start_at=datetime.now() + + timedelta(days=1),
            end_at=datetime.now() + timedelta(days=2),
            status=TimeSale.Status.ACTIVE
        )
        new_timesale.save()

        command = TimeSalePurchaseRequestDto(
            data={
                "user_id": 1,
                "quantity": 10
            }
        )

        # Act
        with pytest.raises(ValueError, match="Time sale is not in valid period"):
            self.sut.purchase_time_sale(new_timesale.timesale_id, command)
