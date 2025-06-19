from django.db import models


class OrderStatus(models.TextChoices):
    PENDING = 'PENDING', '대기중'
    COMPLETED = 'COMPLETED', '완료'
    FAILED = 'FAILED', '실패'
