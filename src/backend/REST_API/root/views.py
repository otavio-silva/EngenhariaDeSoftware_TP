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

    # Analisa se o usuario possui alguma mensagem nao recebida
    try:
        user_messages = Message.objects.filter(receiver=request.user, received_at=None).all()
    except:
        content = {'error: messages cannot be accessed.'}
        print(content)

    # Tenta o envio de cada uma das mensagens
    if len(user_messages) != 0:
        for message in user_messages:

            # Dados para requisicao a ser enviada para o front
            data = {'id':message.id,'sender':message.sender, 'content':message.content, 'created_at':message.created_at}

            # TODO: testar o envio e o recebimento de requisicoes para o front apos a integracao

            try:
                # Promove o envio da mensagem para o frontend, para o usuario de destino
                response = requests.post("http://127.0.0.1:5000/api/messages", data=data)
            except:
                print('error in message id=', message.id, ': request has not been sent to frontend.')

            try:
                # Caso a mensagem seja recebida
                # Insere a data e hora de recebimento da mensagem na instancia da mensagem
                if response.success == True:
                    # alterar
                    message.received_at = datetime.now()
                    message.save()
            except:
                print('error in message id=', message.id, ': frontend request has not been correctly received.')
