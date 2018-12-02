import docker
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import uuid

from apps.strategy import gbot

docker_client = docker.from_env()


class Strategy(models.Model):
    class Meta:
        verbose_name = 'Strategy'
        verbose_name_plural = 'Strategies'

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = JSONField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    port = models.PositiveIntegerField(validators=[MinValueValidator(7000), MaxValueValidator(7500)], unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.pk}. {self.user}'

    def set_value(self, key, value):
        self.data[key] = value
        self.save(update_fields=['data', 'updated_at'])

    def delete_key(self, key):
        self.data.pop(key)
        self.save(update_fields=['data', 'updated_at'])

    def up_container(self):
        env_data = self.data
        env_data.update({
            "WEB_AUTH_KEY": settings.SECRET_KEY,
            "PORT": f'{self.port}'
        })
        try:
            container = docker_client.containers.run(
                name=self.uuid,
                image='gbot',
                network='mitra_mitra',
                environment=env_data,
                ports={f'{self.port}/tcp': self.port},
                detach=True,
                links=[('mitra_web', 'mitra_web'), ]
            )
        except (docker.errors.APIError) as e:
            return e
        return container

    def down_container(self):
        try:
            container = docker_client.containers.get(str(self.uuid))
        except (docker.errors.NotFound, docker.errors.APIError):
            return False
        container.stop()
        container.remove()
        return True

    def close_all_orders(self):
        client = gbot.Client(host=f'http://{str(self.uuid)}', port=f'{self.port}')
        response = client.close_orders()
        return response

    def get_orders(self):
        client = gbot.Client(host=f'http://{str(self.uuid)}', port=f'{self.port}')
        response = client.get_orders()
        return response

    def get_history(self):
        client = gbot.Client(host=f'http://{str(self.uuid)}', port=f'{self.port}')
        response = client.get_history()
        return response

    def restart_container(self):
        try:
            container = docker_client.containers.get(str(self.uuid))
        except (docker.errors.NotFound, docker.errors.APIError):
            return False
        container.restart()
        return True
