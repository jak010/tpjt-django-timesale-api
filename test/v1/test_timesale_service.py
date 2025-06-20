import datetime
from datetime import datetime, timedelta

import pytest

from src.apps.models.product import Product
from src.apps.models.timesale import TimeSale
from src.apps.services.interfaces.i_timesale_service import ITimeSaleService
from src.apps.services.v1.timesale_service import TimeSaleService


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

    # -------------------------------
    # get_timesale()
    # -------------------------------

    def test_get_timesale_success(self):
        """유효한 타임세일 ID에 대해 상세 정보를 정상적으로 조회할 수 있는지 테스트합니다."""

    def test_get_timesale_not_found(self):
        """존재하지 않는 타임세일 ID로 조회 시 예외가 발생하는지를 테스트합니다."""

    # -------------------------------
    # get_ongoing_timesales()
    # -------------------------------

    def test_get_ongoing_timesales_success(self):
        """현재 진행 중인 타임세일이 정상적으로 필터링되고 페이지네이션되어 반환되는지를 테스트합니다."""

    def test_get_ongoing_timesales_empty(self):
        """조건에 해당하는 타임세일이 없을 때 빈 리스트를 반환하는지를 테스트합니다."""

    # -------------------------------
    # purchase_time_sale()
    # -------------------------------

    def test_purchase_timesale_success(self):
        """타임세일 구매 요청이 정상적으로 처리되고 주문 및 재고 차감이 이루어지는지를 테스트합니다."""

    def test_purchase_timesale_out_of_stock(self):
        """재고가 부족한 상황에서 예외가 발생하는지를 테스트합니다."""
