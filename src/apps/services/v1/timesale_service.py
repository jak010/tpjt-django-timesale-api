import datetime

from apps.models import Product, TimeSale
from src.apps.dto.timsale_dto import TimeSaleCreateRequestDto
from src.apps.services.interfaces.i_timesale_service import ITimeSaleService


class TimeSaleService(ITimeSaleService):

    def create_timesale(self,
                        product_id: int,
                        quantity: int,
                        discount_price: int,
                        start_at: datetime.datetime,
                        end_at: datetime.datetime
                        ):
        """ timesale 생성하기 """

        product = Product.objects.filter(product_id=product_id).first()
        if product is None:
            raise Exception("Product Not Found")

        timesale = TimeSale.init_entity(
            product=product,
            quantity=quantity,
            discount_price=discount_price,
            start_at=start_at,
            end_at=end_at
        )
        timesale.save()

        return timesale

    def get_timesale(self, timesale_id: int):
        pass

    def get_ongoing_timesales(self, page: int, size: int):
        pass

    def purchase_time_sale(self, timesale_id: int, command: TimeSaleCreateRequestDto):
        pass
