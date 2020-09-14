from django.http import HttpResponse, JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework import permissions
from rest_framework import generics

from chat.models import Chat
from message.models import Message

from api.serializers import MessageSerializer, UserSerializer
from user.models import User

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = (permissions.IsAuthenticated, )
