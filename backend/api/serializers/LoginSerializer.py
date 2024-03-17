# serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import Assistant





class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None or password is None:
            raise serializers.ValidationError(
                'Please provide both username and password.'
            )

        user = Assistant.objects.filter(username=username).first()

        if user is None:
            raise serializers.ValidationError(
                'No user with this username/password combination.'
            )

        if not user.check_password(password):
            raise serializers.ValidationError(
                'No user with this username/password combination.'
            )

        return user
