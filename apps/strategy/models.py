from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
import uuid


class Strategy(models.Model):
    class Meta:
        verbose_name = 'Strategy'
        verbose_name_plural = 'Strategies'

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = JSONField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}. {}'.format(self.pk, self.user)

    def set_value(self, key, value):  # TODO: !
        self.data[key] = value
        self.save()

