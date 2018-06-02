from django.db import models

from apps.order.models import Exchange


class BTCRates(models.Model):
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    usd_rate = models.DecimalField(blank=True, null=True, decimal_places=8, max_digits=12)

    def __str__(self):
        return '{0}: {1}'.format(self.datetime, self.usd_rate)
