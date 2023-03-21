from django.contrib import admin

from accounts.models.account import Account
from accounts.models.connection import Connection
from accounts.models.profile import Profile
from accounts.models.token import AccountToken


# Register your models here.
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "is_staff", "is_superuser")


@admin.register(AccountToken)
class AccountTokenAdmin(admin.ModelAdmin):
    list_display = ("account", "uuid", "created_at")
    fields = ("account",)
    readonly_fields = ("uuid", "created_at")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("account", "fullname", "phone", "address")
    fields = ("account", "fullname", "phone", "address", "image")
    search_fields = ("fullname", "address")
    readonly_fields = ("account",)


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ("name", "account", "age", "relation")
    search_fields = ("name", "account__name")
    readonly_fields = ("account", "created_at", "updated_at")

    @admin.display()
    def account(self, obj):
        return obj.account.profile.fullname
