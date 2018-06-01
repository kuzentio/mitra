from celery import shared_task
from apps.profile_app import Account
from django.core.management import call_command


@shared_task(bind=True)
def import_bittrex_orders_task(self):
    emails = Account.objects.all().values_list('user__email', flat=True)
    for email in emails:
        call_command('import_bittrex_orders', account_email=email)


