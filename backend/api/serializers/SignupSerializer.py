# serializers.py
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from api.models import Assistant

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    def create(self, validated_data):
        
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    class Meta:
        model = Assistant
        fields = ['first_name', 'last_name', 'username', 'password', 'is_fr', 'is_dz']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'username': {'required': True},
            'password': {'required': True},
            'is_fr': {'required': True},
            'is_dz': {'required': True}
        }
