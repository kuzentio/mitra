from django.contrib import admin

from apps.rates.models import BTCRate


@admin.register(BTCRate)
class BTCRaresAdmin(admin.ModelAdmin):
    list_display = ['id', 'close', 'volume', 'datetime']
