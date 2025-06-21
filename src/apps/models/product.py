from django.db import models

from .abstract import TimestampedModel


class Product(TimestampedModel):
    class Meta:
        db_table = 'products'
        ordering = ['created_at']

    product_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    price = models.BigIntegerField(null=False)
    description = models.TextField(null=False)

    def __str__(self):
        return self.name

    @classmethod
    def init_entity(cls, name: str, price: int, description: str):
        if price is None:
            raise Exception("Product Price is Empty")
        if not isinstance(price, int):
            raise ValueError("Product Price is Invalid Type")
        if price < 0:
            raise Exception("Product Price is Negative")

        if name is None or not name:
            raise Exception("Product Name is Empty")

        if description is None:
            raise Exception("Product Description is Empty")

        return cls(
            name=name,
            price=price,
            description=description
        )
