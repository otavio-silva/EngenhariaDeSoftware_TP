from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from api import views
from message.views import create_message, message_detail

urlpatterns = [
    path('auth', obtain_auth_token),
    path('users/register', views.UserCreate.as_view()),
    path('users/<int:pk>', views.UserDetail.as_view()),
    path('messages', create_message),
    path('messages/<int:pk>', message_detail)
]
