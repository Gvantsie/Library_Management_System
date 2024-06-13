import datetime

import jwt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
import requests
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from library.models.user_stats import UserStatistics
from library.serializers.user_stats_serializer import UserStatisticsSerializer
from users.forms import UserLoginForm, CustomUserCreationForm
from users.models import CustomUser
from users.serializers import UserSerializer, User, UserLoginSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model, authenticate, login
from django.http import JsonResponse

UserModel = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return JsonResponse({'success': False, 'errors': serializer.errors}, status=400)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(user)
        return Response(serializer.data)


class UserLoginView(ObtainAuthToken):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        response = super(UserLoginView, self).post(request, *args, **kwargs)
        token = response.data['token']
        user = UserModel.objects.get(auth_token=token)
        return JsonResponse({'token': token, 'user_id': user.pk})


class CustomAuthToken(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise InvalidToken(e)

        response_data = serializer.validated_data
        response_data['email'] = serializer.user.email

        return Response(response_data, status=status.HTTP_200_OK)


class UserStatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_stats, created = UserStatistics.objects.get_or_create(user=request.user)
        serializer = UserStatisticsSerializer(user_stats)
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = CustomUser.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
            'iat': datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class UserView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        # Extract the token from the Authorization header (Bearer <token>)
        try:
            token = token.split()[1]  # Assuming the format is "Bearer <token>"
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = CustomUser.objects.filter(id=payload['id']).first()

        if not user:
            raise AuthenticationFailed('User not found')

        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()

        response.delete_cookie('jwt')

        response.data = {
            'message': 'success'
        }

        return response


def register(request):
    if request.method == 'POST':
        response = requests.post('http://localhost:8000/auth/create-user/', data=request.POST)
        if response.status_code == 200:
            return redirect('success_page')  # Redirect to a success page
        else:
            return render(request, 'user/register.html', {'error': response.json()})
    return render(request, 'user/register.html')
