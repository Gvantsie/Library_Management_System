from rest_framework import generics
from .serializers import UserSerializer
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserCreateView(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
