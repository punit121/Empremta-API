from rest_framework import serializers
from .models import File

class EmbedSerializer(serializers.ModelSerializer):
    class Meta:
        model = File