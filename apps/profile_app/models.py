from django.contrib.auth.models import User
from django.db import models

from apps.order.models import Exchange


class Legal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=255)
    middlename = models.CharField(max_length=255, blank=True, null=True)
    secondname = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)


class Account(models.Model):
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    exchange: Exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    email: str = models.EmailField(blank=True, null=True)
    username: str = models.CharField(max_length=255)
    password: str = models.CharField(max_length=255)
    api_key: str = models.CharField(max_length=255, blank=True, null=True)
    api_secret: str = models.CharField(max_length=255, blank=True, null=True)
    is_active: bool = models.BooleanField(default=True, help_text='Is active account on exchange')


class HerokuCredentials(models.Model):
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    api_key: str = models.CharField(max_length=255, unique=True)
