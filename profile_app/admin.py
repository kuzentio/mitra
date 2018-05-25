from django.contrib import admin
from profile_app.models import Legal, Account


@admin.register(Legal)
class LegalAdmin(admin.ModelAdmin):
    pass


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('exchange_name', 'username', 'password')

    def exchange_name(self, obj):
        return obj.exchange.name
