from django.contrib import admin
from apps.strategy.models import Strategy


@admin.register(Strategy)
class StrategiesAdmin(admin.ModelAdmin):
    list_display = ['user', 'data', 'created_at', 'updated_at']
    ordering = ['updated_at', ]
