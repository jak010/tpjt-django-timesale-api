from django.db import models

from .timesale import TimeSale

from .abstract import TimestampedModel


class TimeSaleOrder(TimestampedModel):
    class Meta:
        db_table = 'time_sale_orders'

    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'

    timesale_order_id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField(null=False)
    time_sale = models.ForeignKey(TimeSale, on_delete=models.CASCADE, related_name='orders')
    quantity = models.BigIntegerField(null=False)
    discount_price = models.BigIntegerField(null=False)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        null=False,
    )

    @classmethod
    def init_entity(cls,
                    user_id: int,
                    timesale: TimeSale,
                    quantity: int,
                    discount_price: int
                    ):
        return cls(
            user_id=user_id,
            time_sale=timesale,
            quantity=quantity,
            discount_price=discount_price,
            status=cls.OrderStatus.PENDING
        )

    def complete(self):
        self.status = TimeSaleOrder.OrderStatus.COMPLETED
        self.save(update_fields=['status', 'updated_at'])

    def fail(self):
        self.status = TimeSaleOrder.OrderStatus.FAILED
        self.save(update_fields=['status', 'updated_at'])
