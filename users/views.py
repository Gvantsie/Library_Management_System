from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.authtoken.views import ObtainAuthToken
import requests
from rest_framework.decorators import api_view
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


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class UserLoginView(ObtainAuthToken):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        response = super(UserLoginView, self).post(request, *args, **kwargs)
        token = response.data['token']
        user = UserModel.objects.get(auth_token=token)
        return JsonResponse({'token': token, 'user_id': user.pk})


class UserStatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_stats, created = UserStatistics.objects.get_or_create(user=request.user)
        serializer = UserStatisticsSerializer(user_stats)
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.filter(username=username).first()
        if user is None or not user.check_password(password):
            return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })


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


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        # Process the form data
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the user or perform user creation logic
            user = form.save()
            return JsonResponse({'success': True, 'message': 'User created successfully!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def register(request):
    if request.method == 'POST':
        response = requests.post('http://localhost:8000/auth/create-user/', data=request.POST)
        if response.status_code == 200:
            return redirect('success_page')  # Redirect to a success page
        else:
            return render(request, 'user/register.html', {'error': response.json()})
    return render(request, 'user/register.html')


@api_view(['POST'])
class LoginView(APIView):
    def post(self, request: Request) -> Response:
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh: RefreshToken = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
