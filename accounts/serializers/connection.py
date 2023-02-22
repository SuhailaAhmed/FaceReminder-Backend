from rest_framework import serializers
from accounts.models.connection import Connection


class ConnectionSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="account.email", read_only=True)

    class Meta:
        model = Connection
        extra_fields = ["email"]
        exclude = ["account"]
