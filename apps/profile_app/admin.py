from django.contrib import admin
from apps.profile_app.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('exchange_name', 'username', 'password')

    def exchange_name(self, obj):
        return obj.exchange.name
