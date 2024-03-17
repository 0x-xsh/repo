# serializers.py
from rest_framework import serializers

from api.models import Assistant

class AssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assistant
        fields = ['first_name', 'last_name', 'username', 'is_fr', 'is_dz']
       
