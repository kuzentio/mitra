from django.contrib import admin
from order.models import Order, Exchange


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'uuid', 'pair', 'type', 'closed_at', 'opened_at']
    search_fields = ['pair']


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ['name', ]
