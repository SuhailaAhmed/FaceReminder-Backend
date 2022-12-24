from django.contrib import admin
from accounts.models.account import Account
from accounts.models.token import AccountToken


# Register your models here.
admin.site.register(Account) 
admin.site.register(AccountToken) 