from django.db import models
from django.utils import timezone

from src.contrib.timestamp_models import TimestampedModel
from .product import Product


class TimeSale(TimestampedModel):
    class Meta:
        db_table = 'time_sales'
        ordering = ["-created_at"]

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        INACTIVE = 'INACTIVE', 'Inactive'

    timesale_id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='time_sales')
    quantity = models.BigIntegerField(null=False)
    remaining_quantity = models.BigIntegerField(null=False)
    discount_price = models.BigIntegerField(null=False)
    start_at = models.DateTimeField(null=False)
    end_at = models.DateTimeField(null=False)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        null=False
    )
    version = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def is_active(self):
        return self.status == TimeSale.Status.ACTIVE

    def purchase(self, quantity):
        self._validate_purchase(quantity)
        self.remaining_quantity -= quantity
        self.save(update_fields=['remaining_quantity'])

    def _validate_purchase(self, quantity):
        self._validate_status()
        self._validate_quantity(quantity)
        self._validate_period()

    def _validate_status(self):
        if self.status != TimeSale.Status.ACTIVE:
            raise ValueError("Time sale is not active")

    def _validate_quantity(self, quantity):
        if self.remaining_quantity < quantity:
            raise ValueError("Not enough quantity available")

    def _validate_period(self):
        now = timezone.now()
        if now < self.start_at or now > self.end_at:
            raise ValueError("Time sale is not in valid period")
