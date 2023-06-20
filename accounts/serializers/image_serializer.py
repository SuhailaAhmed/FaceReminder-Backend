from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers


class ImageSerializer(serializers.Serializer):
    image = Base64ImageField()
