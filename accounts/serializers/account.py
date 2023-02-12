from rest_framework import serializers
from accounts.models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ('is_staff', 'is_superuser', 'groups', 'user_permissions')