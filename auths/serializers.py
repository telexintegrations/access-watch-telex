from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',
            'is_superuser',
            'password'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=15)
    password = serializers.CharField(max_length=15)
