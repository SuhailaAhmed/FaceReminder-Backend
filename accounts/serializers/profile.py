from rest_framework import serializers
from accounts.models.profile import Profile

class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='account.email', read_only=True)
    
    class Meta:
        model= Profile
        fields = '__all__'
        extra_fields = ['email']