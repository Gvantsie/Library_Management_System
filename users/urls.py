from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from users.views import UserCreateView, UserDetailView, UserLoginView, login_, register, library_home

urlpatterns = [
    path('create-user/', UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('auth/', obtain_auth_token, name='auth'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('login_/', login_, name='login_'),
    path('library/', library_home, name='library_home'),
    path('register/', register, name='register_user'),

]