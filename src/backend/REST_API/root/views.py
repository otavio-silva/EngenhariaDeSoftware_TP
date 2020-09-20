import requests

from django.http.request import QueryDict

from django.http import HttpResponse, JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework import permissions
from rest_framework import generics
from rest_framework import status

from datetime import datetime

from user.models import User
from user.serializers import UserSerializer

from message.models import Message
from message.serializers import MessageSerializer


def check_message(request):
    # Verifica se um determinado usuario possui mensagens para serem recebidas
    # Caso possua, promove o recebimento delas e a alteracao no BD

    user_messages = Message.objects.filter(receiver=request.user, received_at=None).all()

    if len(user_messages) != 0:
        for message in user_messages:
            data = {'id': message.id,'sender': message.sender, 'content': message.content, 'created_at': message.created_at}


            try:
                # Promove o envio da mensagem para o frontend
                response = requests.post("http://127.0.0.1:5000/api/messages", data=data)
            except:
                content = {'error': f'"{message.id}" has not been sent.'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)


            # Caso a mensagem seja recebida
            if response.success == True:
                message.received_at = datetime.now()
                message.save()

            # Insere a data e a hora de leitura da mensagem