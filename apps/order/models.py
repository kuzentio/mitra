from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models

from apps.order import constants


class Exchange(models.Model):
    name = models.CharField(max_length=255, choices=constants.EXCHANGES_CHOICES, unique=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.get_name_display()


class Order(models.Model):
    ORDER_TYPE_CHOICES = (
        (constants.ORDER_TYPE_BUY, constants.ORDER_TYPE_BUY.lower()),
        (constants.ORDER_TYPE_SELL, constants.ORDER_TYPE_SELL.lower()),
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


class Price(models.Model):
    pair = models.CharField(max_length=10, unique=True)
    ask = models.DecimalField(decimal_places=8, max_digits=12)
    bid = models.DecimalField(decimal_places=8, max_digits=12)
    timestamp = models.DateTimeField(blank=True, null=True)
    data = JSONField(blank=True, null=True)

    def __str__(self):
        return '{0}: {1}'.format(self.pair, self.ask)
