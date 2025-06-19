from django.db import models


class TimeSaleStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    SOLD_OUT = 'SOLD_OUT', 'Sold Out'
    ENDED = 'ENDED', 'Ended'
