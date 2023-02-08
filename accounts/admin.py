from django.contrib import admin
from accounts.models.account import Account
from accounts.models.token import AccountToken
from accounts.models.profile import Profile


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
