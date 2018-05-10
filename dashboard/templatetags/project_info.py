from django import template

from config import settings
from order.models import Exchange

register = template.Library()


@register.simple_tag
def project_name():
    return getattr(settings, 'PROJECT_NAME', '')


@register.simple_tag
def exchanges_online():
    exchanges = Exchange.objects.filter(is_active=True)
    return exchanges
