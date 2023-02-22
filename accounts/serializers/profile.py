from rest_framework import serializers
from accounts.models import Profile
from drf_extra_fields.fields import Base64ImageField

class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source = 'account.email', read_only = True)
    image = Base64ImageField()

    class Meta:
        model = Profile
        extra_fields = ['email']
        exclude = ['account']