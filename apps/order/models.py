from django.contrib.postgres.fields import JSONField
from django.db import models

from apps.order import constance


class Exchange(models.Model):
    name = models.CharField(max_length=255, choices=constance.EXCHANGES_CHOICES, unique=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.get_name_display()


class Order(models.Model):
    ORDER_TYPE_CHOICES = (
        (constance.ORDER_TYPE_BUY, constance.ORDER_TYPE_BUY.lower()),
        (constance.ORDER_TYPE_SELL, constance.ORDER_TYPE_SELL.lower()),
    )
    uuid = models.UUIDField(max_length=255, blank=True, null=True, help_text='Remote unique identifier')
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    account = models.ForeignKey('profile_app.Account', on_delete=models.CASCADE)

    type = models.CharField(max_length=5, choices=ORDER_TYPE_CHOICES)
    pair = models.CharField(max_length=20)

    quantity = models.DecimalField(blank=True, null=True, decimal_places=8, max_digits=12)
    commission = models.DecimalField(blank=True, null=True, decimal_places=8, max_digits=12)
    price = models.DecimalField(blank=True, null=True, decimal_places=8, max_digits=12)

    opened_at = models.DateTimeField(blank=True, null=True)
    closed_at = models.DateTimeField(blank=True, null=True)

    data = JSONField(default=dict, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['uuid', ])
        ]
