from django.db import models


class Rate(models.Model):
    date = models.DateField()
    btc_rate = models.DecimalField()

