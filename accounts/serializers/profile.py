from rest_framework import serializers
from accounts.models.profile import Profile

class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='account.email', read_only=True)
    
    class Meta:
        model= Profile
        extra_fields = ['email']
        exclude = ['account']