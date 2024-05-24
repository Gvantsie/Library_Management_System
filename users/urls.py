from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from users.views import UserCreateView, UserDetailView

urlpatterns = [
    path('users/', UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('auth/', obtain_auth_token, name='auth'),
]