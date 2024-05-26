from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, label="Confirm Password", style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'personal_number', 'birth_date', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}, 'password2': {'write_only': True, 'style': {'input_type': 'password'}}}

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            personal_number=validated_data['personal_number'],
            birth_date=validated_data['birth_date'],
            is_staff=False  # Ensure that new users registered via the API are not staff
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""

    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        """Validate and authenticate the user"""
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)

            if not user:
                msg = _('Unable to authenticate with provided credentials')

