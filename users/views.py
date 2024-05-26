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
from rest_framework_simplejwt.tokens import RefreshToken

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
    # authentication_classes = (TokenAuthentication,)  # we have to add header with our authentication token
    permission_classes = (IsAuthenticated,)


class UserLoginView(ObtainAuthToken):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        response = super(UserLoginView, self).post(request, *args, **kwargs)
        token = response.data['token']
        user = UserModel.objects.get(auth_token=token)
        return JsonResponse({'token': token, 'user_id': user.pk})


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        }, status=status.HTTP_200_OK)


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
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
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
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = CustomUser.objects.filter(id=payload['id']).first()

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

# def library_home(request):
#     # Check if the user is authenticated
#     if not request.user.is_authenticated:
#         return redirect('login_')
#
#     # Render the library home page
#     return render(request, 'home.html')


# @login_required
# def user_page(request):
#     # Fetch all books
#     books_response = requests.get(request.build_absolute_uri('/books/'))
#     books = books_response.json()
#
#     # Fetch popular books
#     popular_books_response = requests.get(request.build_absolute_uri('/statistics/popular-books/'))
#     popular_books = popular_books_response.json()
#
#     # Fetch book statistics
#     book_stats_response = requests.get(request.build_absolute_uri('/statistics/book-stats/'))
#     book_stats = book_stats_response.json()
#
#     context = {
#         'books': books,
#         'form': form,
#         'popular_books': popular_books,
#         'book_stats': book_stats,
#     }
#
#     return render(request, 'user/user_page.html', context)


# @csrf_exempt
# def create_user(request):
#     if request.method == 'POST':
#         # Process the form data
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             # Save the user or perform user creation logic
#             user = form.save()
#             return JsonResponse({'success': True, 'message': 'User created successfully!'})
#         else:
#             return JsonResponse({'success': False, 'errors': form.errors}, status=400)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)


def register(request):
    if request.method == 'POST':
        response = requests.post('http://localhost:8000/auth/create-user/', data=request.POST)
        if response.status_code == 200:
            return redirect('success_page')  # Redirect to a success page
        else:
            return render(request, 'user/register.html', {'error': response.json()})
    return render(request, 'user/register.html')
