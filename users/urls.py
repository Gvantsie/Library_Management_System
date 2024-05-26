from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView

from library.views.book import BookListView
from library.views.reservation import ReserveBookView
from users.views import (RegisterView,
                         UserDetailView,
                         UserStatisticsView,
                         LoginView,
                         CustomAuthToken,
                         )

urlpatterns = [
    path('create-user/', RegisterView.as_view(), name='user-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('auth/', obtain_auth_token, name='auth'),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    # path('login/', UserLoginView.as_view(), name='login'),
    # path('register/', register, name='register_user'),

    path('login/', LoginView.as_view(), name='login'),
    path('books/', BookListView.as_view(), name='book-list'),
    path('statistics/', UserStatisticsView.as_view(), name='user-statistics'),
    path('reserve/', ReserveBookView.as_view(), name='reserve-book'),
]



