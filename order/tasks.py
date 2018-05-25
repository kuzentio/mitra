from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model

from order.models import Order


# @shared_task(name='order.tasks.debug_task', bind=True)
@shared_task(bind=True)
def debug_task(self):
    UserModel = get_user_model()
    result = UserModel.objects.all().values_list('email', flat=True)
    print(' '.join(result))
    print('------------------------------------')
    print('------------------------------------')
    print('------------------------------------')
    print(settings.INSTALLED_APPS)
    print([o.id for o in Order.objects.all()])


