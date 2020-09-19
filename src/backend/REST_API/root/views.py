import requests

from django.http.request import QueryDict

from django.http import HttpResponse, JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework import permissions
from rest_framework import generics
from rest_framework import status

from user.models import User
from user.serializers import UserSerializer

from message.models import Message
from message.serializers import MessageSerializer

def check_message(user):
    # Verifica se um determinado usuario possui mensagens para serem recebidas

    user_receiver = user.id

    user_messages = Message.objects.filter(receiver=user, received_at=None).all()

    if len(user_messages) != 0:
        for message in user_messages:
            print(message.created_at)
