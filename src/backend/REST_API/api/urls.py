from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from user.views import create_user, user_detail, user_keep_active
from message.views import create_message, message_detail

urlpatterns = [
    path('auth', obtain_auth_token),
    path('keep-active', user_keep_active),
    path('users/register', create_user),
    path('users/<slug:username>', user_detail),
    path('messages', create_message),
    path('messages/<int:pk>', message_detail)
]
