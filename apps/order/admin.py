from django.contrib import admin
from apps.order.models import Order, Exchange, Price


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'uuid', 'pair', 'type', 'price', 'quantity', 'closed_at', 'opened_at']
    search_fields = ['pair']


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ['pair', 'ask', 'timestamp']
