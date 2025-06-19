from django.db import models

from .timesale import TimeSale


class TimeSaleOrder(models.Model):
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
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        db_table = 'time_sale_orders'

    def complete(self):
        self.status = TimeSaleOrder.OrderStatus.COMPLETED
        self.save(update_fields=['status', 'updated_at'])

    def fail(self):
        self.status = TimeSaleOrder.OrderStatus.FAILED
        self.save(update_fields=['status', 'updated_at'])
