from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView

from library.views.book import BookListView
from library.views.reservation import ReserveBookView
from users.views import (RegisterView,
                         UserDetailView,
                         UserStatisticsView,
                         LoginView,
                         UserView, LogoutView, register, CustomAuthToken,
                         )

urlpatterns = [
    path('create-user/', RegisterView.as_view(), name='user-create'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserView.as_view(), name='user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('token/obtain/', CustomAuthToken.as_view(), name='token_obtain'),
    path('statistics/', UserStatisticsView.as_view(), name='user-statistics'),
    path('book/<int:book_id>/reserve/', ReserveBookView.as_view(), name='reserve-book'),
    path('register/', register, name='register'),

]



