from rest_framework import serializers
from .models import Songs


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)


class SongsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Songs
        fields = ("title", "artist")
