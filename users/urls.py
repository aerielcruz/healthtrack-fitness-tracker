from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views
from .views import RegisterView, UserView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('user/', UserView.as_view(), name='user'),
]