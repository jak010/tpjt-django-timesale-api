import datetime

from apps.models import Product, TimeSale, TimeSaleOrder
from src.apps.dto.timsale_dto import TimeSaleCreateRequestDto
from src.apps.services.interfaces.i_timesale_service import ITimeSaleService

from django.db import transaction


class TimeSaleService(ITimeSaleService):

    @transaction.atomic()
    def create_timesale(self,
                        product_id: int,
                        quantity: int,
                        discount_price: int,
                        start_at: datetime.datetime,
                        end_at: datetime.datetime
                        ):
        """ timesale 생성하기


        Implementation
            상품 ID에 기반하여 주어진 수량, 할인 가격, 시작/종료 시간으로 유효한 타임세일(TimeSale) 엔티티를 생성하고 저장한 뒤, 이를 반환

        Ref
            - 테스트 참조 : test_timesale_service.py

        TODO
            - 25.06.21 : Argument를 Object로 Refactoring 하기
        """

        product = Product.objects.filter(product_id=product_id).first()
        if product is None:
            raise Exception("Product Not Found")

        self._validate_time_sale(
            quantity,
            discount_price,
            start_at, end_at
        )

        timesale = TimeSale.init_entity(
            product=product,
            quantity=quantity,
            discount_price=discount_price,
            start_at=start_at,
            end_at=end_at
        )
        timesale.save()

        return timesale

    def get_timesale(self, timesale_id: int) -> TimeSale:
        """ 타임세일 조회하기

        """

        timesale = TimeSale.objects.filter(timesale_id=timesale_id).first()
        if timesale is None:
            raise Exception("TimeSale Not Found")
        return timesale

    def get_ongoing_timesales(self, page: int, size: int):
        """ 진행중인 타임세일 조회하기

        TODO:
            - 25.06.21 : Pagination 적용하기

        """

        ongoging_timesale = TimeSale.objects.filter(status=TimeSale.ACTIVE.value)

        return ongoging_timesale.all()

    @transaction.atomic()
    def purchase_time_sale(self, timesale_id: int, command: TimeSaleCreateRequestDto):
        """ 타임 세일 상품 구매하기

        """

        timesale = TimeSale.objects.select_for_update().filter(timesale_id=timesale_id).first()
        if timesale is None:
            raise Exception("TimeSale Not Found")

        timesale.purchase(command.quantity)
        timesale.save()

        timesale_order = TimeSaleOrder.init_entity(
            timesale=timesale,
            user_id=command.user_id,
            quantity=command.quantity,
            discount_price=timesale.discount_price
        )
        timesale_order.save()
        timesale_order.complete()

        return timesale

    @classmethod
    def _validate_time_sale(cls, quantity: int, discount_price: int, start_at: datetime.datetime, end_at: datetime.datetime):
        if start_at > end_at:
            raise Exception("End At must be greater than Start At")

        if quantity <= 0:
            raise Exception("Quantity must be greater than 0")

        if discount_price <= 0:
            raise Exception("Discount Price must be greater than 0")
