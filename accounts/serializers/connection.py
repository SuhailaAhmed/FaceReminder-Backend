from rest_framework import serializers
from accounts.models import connection

class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = connection
        fields = '__all__'