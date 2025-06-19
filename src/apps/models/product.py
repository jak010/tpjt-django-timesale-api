from django.db import models

from src.contrib.timestamp_models import TimestampedModel


class Product(TimestampedModel):
    class Meta:
        db_table = 'products'
        ordering = ['created_at']
        app_label = "apps"

    product_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    price = models.BigIntegerField(null=False)
    description = models.TextField(null=False)

    def __str__(self):
        return self.name

    @classmethod
    def init_entity(cls, name: str, price: int, description: str):
        return cls(
            name=name,
            price=price,
            description=description
        )
