from django.contrib.postgres.fields import JSONField
from django.db import models

from apps.order.models import Exchange


class BTCRate(models.Model):
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)

    high = models.DecimalField(decimal_places=8, max_digits=20)
    open = models.DecimalField(decimal_places=8, max_digits=20)
    close = models.DecimalField(decimal_places=8, max_digits=20)
    low = models.DecimalField(decimal_places=8, max_digits=20)
    volume = models.DecimalField(decimal_places=8, max_digits=20)
    base_volume = models.DecimalField(decimal_places=8, max_digits=20)
    datetime = models.DateTimeField()

    data = JSONField(default=dict)

    def __str__(self):
        return '{0}: {1}'.format(self.datetime, self.close)
