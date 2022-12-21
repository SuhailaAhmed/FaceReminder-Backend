from django.contrib import admin
from accounts.models.account import Account
from accounts.models.tokens import AccountToken


# Register your models here.
admin.site.register(Account)

@admin.register(AccountToken)
class AccountTokenAdmin(admin.ModelAdmin):
    list_display = ('account', 'uuid', 'created_at')
    fields = ('account',)
    readonly_fields = ('uuid', 'created_at')
