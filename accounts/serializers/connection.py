from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from accounts.models.connection import Connection


class ConnectionSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Connection
        exclude = ["account"]
