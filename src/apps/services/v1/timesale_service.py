import datetime

from django.db import transaction
from rest_framework.exceptions import APIException
from rest_framework.pagination import LimitOffsetPagination

from apps.dto.timsale_dto import TimeSaleCreateRequestDto, TimeSalePurchaseRequestDto
from apps.models import Product, TimeSale, TimeSaleOrder
from apps.services.interfaces.i_timesale_service import ITimeSaleService


class TimeSaleService(ITimeSaleService):

    @transaction.atomic()
    def create_timesale(self, command: TimeSaleCreateRequestDto) -> TimeSale:
        """ 타임세일 생성하기

        Implementation
            `command` 객체에 포함된 상품 ID, 수량, 할인 가격, 시작/종료 시간을 사용하여 유효한 타임세일(TimeSale) 엔티티를 생성하고 저장한 뒤, 이를 반환

        Side Effects
        - 새로운 `TimeSale` 엔티티가 데이터베이스에 생성 및 저장됩니다.
        - 유효하지 않은 입력(예: 존재하지 않는 상품 ID, 유효하지 않은 시간 범위, 0 이하의 수량/할인 가격)의 경우 예외가 발생하여 타임세일 생성이 실패할 수 있습니다.

        """

        product = Product.objects.filter(product_id=command.validated_data["product_id"]).first()
        if product is None:
            raise Exception("Product Not Found")

        self._validate_time_sale(
            command.validated_data["quantity"],
            command.validated_data["discount_price"],
            command.validated_data["start_at"],
            command.validated_data["end_at"]
        )

        timesale = TimeSale.init_entity(
            product=product,
            quantity=command.validated_data["quantity"],
            discount_price=command.validated_data["discount_price"],
            start_at=command.validated_data["start_at"],
            end_at=command.validated_data["end_at"],
            status=TimeSale.Status.ACTIVE
        )
        timesale.save()

        return timesale

    def get_timesale(self, timesale_id: int) -> TimeSale:
        """ 특정 타임세일 정보를 조회합니다.

        Args:
            timesale_id (int): 조회할 타임세일의 고유 ID.

        Returns:
            TimeSale: 조회된 TimeSale 엔티티.

        Raises:
            Exception: 해당 `timesale_id`를 가진 타임세일이 없을 경우 "TimeSale Not Found" 예외를 발생시킵니다.
        """

        from rest_framework.exceptions import NotFound

        timesale = TimeSale.objects.filter(timesale_id=timesale_id).first()
        if timesale is None:
            raise NotFound()
        return timesale

    def get_ongoing_timesales(self, page: int, size: int):
        """ 진행중인 타임세일 조회하기

        TODO:
            - 25.06.21 : Pagination 적용하기

        """

        class RequestParam:
            def __init__(self, limit: int, offset: int):
                self.query_params = {
                    "limit": limit,
                    "offset": offset
                }

        limit_pagination = LimitOffsetPagination()

        return limit_pagination.paginate_queryset(
            TimeSale.objects.filter(status=TimeSale.Status.ACTIVE).all(),
            RequestParam(limit=size, offset=page),
            None
        )

    @transaction.atomic()
    def purchase_time_sale(self, timesale_id: int, command: TimeSalePurchaseRequestDto) -> TimeSale:
        """ 타임 세일 상품 구매하기

        이 함수는 특정 타임세일 상품을 구매하는 로직을 처리합니다.
        구매 요청의 유효성을 검사하고, 타임세일 재고를 업데이트하며, 구매 주문을 생성합니다.

        Args:
            timesale_id (int): 구매할 타임세일 상품의 고유 ID.
            command (TimeSalePurchaseRequestDto): 구매 요청에 필요한 정보를 담고 있는 DTO 객체.
                (예: 구매 수량, 사용자 ID 등)

        Returns:
            TimeSale: 구매가 완료된 타임세일 엔티티.

        Raises:
            Exception:
                - `timesale_id`에 해당하는 타임세일 상품을 찾을 수 없을 경우 "TimeSale Not Found" 예외를 발생시킵니다.
                - 구매 수량이 타임세일 재고를 초과하는 경우 `timesale.purchase()` 메서드 내부에서 예외가 발생할 수 있습니다.
                - `command` 객체의 유효성 검사에 실패할 경우 예외가 발생합니다.

        Side Effects:
            - `TimeSale` 엔티티의 `quantity` 필드가 구매 수량만큼 감소합니다.
            - 새로운 `TimeSaleOrder` 엔티티가 데이터베이스에 생성 및 저장됩니다.
            - 데이터베이스 트랜잭션 내에서 모든 작업이 원자적으로 처리됩니다.
        """

        timesale = TimeSale.objects.select_for_update().filter(timesale_id=timesale_id).first()
        if timesale is None:
            raise Exception("TimeSale Not Found")

        try:
            timesale.purchase(command.validated_data["quantity"])
        except Exception as e:
            print(e)
            raise APIException()

        timesale.save()

        timesale_order = TimeSaleOrder.init_entity(
            user_id=command.validated_data['user_id'],
            quantity=command.validated_data["quantity"],
            timesale=timesale,
            discount_price=timesale.discount_price
        )
        timesale_order.save()
        timesale_order.complete()

        return timesale

    @classmethod
    def _validate_time_sale(cls, quantity: int, discount_price: int, start_at: datetime.datetime, end_at: datetime.datetime):
        """ 타임세일 생성에 필요한 값들을 검증합니다.

        Args:
            quantity (int): 타임세일 상품의 수량. 0보다 커야 합니다.
            discount_price (int): 타임세일 상품의 할인 가격. 0보다 커야 합니다.
            start_at (datetime.datetime): 타임세일 시작 시간.
            end_at (datetime.datetime): 타임세일 종료 시간. 시작 시간보다 늦어야 합니다.

        Raises:
            Exception:
                - `end_at`이 `start_at`보다 빠를 경우 "End At must be greater than Start At" 예외를 발생시킵니다.
                - `quantity`가 0 이하일 경우 "Quantity must be greater than 0" 예외를 발생시킵니다.
                - `discount_price`가 0 이하일 경우 "Discount Price must be greater than 0" 예외를 발생시킵니다.
        """
        if start_at > end_at:
            raise Exception("End At must be greater than Start At")

        if quantity <= 0:
            raise Exception("Quantity must be greater than 0")

        if discount_price <= 0:
            raise Exception("Discount Price must be greater than 0")
