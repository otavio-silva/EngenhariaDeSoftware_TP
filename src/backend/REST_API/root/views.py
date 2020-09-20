import requests

from django.http.request import QueryDict

from django.http import HttpResponse, JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework import permissions
from rest_framework import generics
from rest_framework import status

from django.utils import timezone

from user.models import User
from user.serializers import UserSerializer

from message.models import Message
from message.serializers import MessageSerializer


def check_messages(request):
    # Verifica se um determinado usuario possui mensagens para serem recebidas
    # Caso possua, promove o recebimento delas e a alteracao no BD

    # Analisa se o usuario possui alguma mensagem nao recebida
    try:
        user_messages = Message.objects.filter(receiver=request.user, received_at=None).all()
    except:
        print('error: messages cannot be accessed.')

    # Tenta o envio de cada uma das mensagens
    if len(user_messages) != 0:
        for message in user_messages:

            # Dados para requisicao a ser enviada para o front
            data = {'id':message.id, 'sender':message.sender, 'content':message.content, 'created_at':message.created_at}

            # TODO: testar o envio e o recebimento de requisicoes para o front apos a integracao

            # Recuperando a instancia de um determinado usuario do BD - exemplo: 'message.sender' eh o ID de um determinado usuario
            # user = User.objects.get(id=message.sender)

            try:
                # Promove o envio da mensagem para o frontend, para o usuario de destino
                response = requests.post("http://localhost:port/api/messages", data=data)
            except:
                print('error in message id=', message.id, ': request has not been sent to frontend.')

            try:
                # Caso a mensagem seja recebida
                # Insere a data e hora de recebimento da mensagem na instancia da mensagem
                if response.success == True:

                    message.received_at = timezone.now()
                    message.save()

                    # Notifica quem enviou a mensagem que ela foi recebida pelo destinatario
                    notify_user_received(message.id)
            except:
                print('error in message id=', message.id, ': frontend request has not been correctly receive.')


def notify_user_read(id):
    # Notifica um usuario de que a mensagem enviada por ele foi lida pelo destinatario

    user_adress =  'http://localhost:port/api/messages/' + str(id)
    data = {'read': True}
    try:
        response = requests.put(user_adress, data=data)
        if response.success != True:
            print('error: read notification of message', id, 'has not been received at frontend.')
    except:
        print('error: read notification of message', id, 'has not been sent to frontend.')


def notify_user_received(id):
    # Notifica um usuario de que a mensagem enviada por ele foi recebida pelo destinatario

    user_adress =  'http://localhost:port/api/messages/' + str(id)
    data = {'received': True}
    try:
        response = requests.put(user_adress, data=data)
        if response.success != True:
            print('error: received notification of message', id, 'has not been received at frontend.')
    except:
        print('error: received notification of message', id, 'has not been sent to frontend.')
