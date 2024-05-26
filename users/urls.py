from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView

from library.views.book import BookListView
from library.views.reservation import ReserveBookView
from users.views import (RegisterView,
                         UserDetailView,
                         UserStatisticsView,
                         LoginView,
                         CustomAuthToken, UserView, LogoutView,
                         )

urlpatterns = [
    path('create-user/', RegisterView.as_view(), name='user-create'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserView.as_view(), name='user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    # path('auth/', obtain_auth_token, name='auth'),
    # path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),



    path('books/', BookListView.as_view(), name='book-list'),
    path('statistics/', UserStatisticsView.as_view(), name='user-statistics'),
    path('reserve/', ReserveBookView.as_view(), name='reserve-book'),
]



