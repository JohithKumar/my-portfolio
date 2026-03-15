from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('users/me/', current_user),
    path('users/', user_list),
    path('users/<uuid:id>/', user_detail),
    path('register/', register),
    path('token/', custom_token_obtain, name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]