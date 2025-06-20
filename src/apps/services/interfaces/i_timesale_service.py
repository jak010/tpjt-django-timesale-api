from abc import abstractmethod
from datetime import datetime

from src.apps.dto.timsale_dto import TimeSaleCreateRequestDto


class ITimeSaleService:

    @abstractmethod
    def create_timesale(self,
                        *,
                        product_id: int,
                        quantity: int,
                        discount_price: int,
                        start_at: datetime,
                        end_at: datetime
                        ):
        """ 시간할인 생성하기 """
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_timesale(self, timesale_id: int):
        """ 시간할인 조회하기

        Args:
            timesale_id (int): 시간할인번호

        """
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_ongoing_timesales(self, page: int, size: int):
        """ 현재 진행 중인 타임세일 목록을 조회합니다.

        타임세일의 시작 시간이 현재 시간 이전이며, 종료 시간이 현재 시간 이후이고,
        상태가 ACTIVE인 타임세일을 페이지네이션하여 반환합니다.

        """
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def purchase_time_sale(self,
                           timesale_id: int,
                           command: TimeSaleCreateRequestDto
                           ):
        """ 타임세일 구매 처리
        타임세일 ID로 해당 상품 조회 비관적 락을 사용하여 조회

        재고 차감 후
            - 타임세일 저장
            - 주문 객체 생성
            - 주문 정보 저장 및 상태 완료

        최종적으로 타임세일 반환

        Parameters:
            timesale_id (Long):
                타임세일 ID
            command (TimeSaleCreateRequestDto):
                구매 요청 정보

        """
        raise NotImplementedError("Method not implemented")
