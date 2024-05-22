from rest_framework import serializers
from users.models import CustomUser
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'personal_number', 'birth_date', 'password')

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            personal_number=validated_data['personal_number'],
            birth_date=validated_data['birth_date'],
            password=validated_data['password']
        )
        return user
