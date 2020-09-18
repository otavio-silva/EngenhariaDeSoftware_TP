from datetime import datetime
from django.http.request import QueryDict

from django.http import HttpResponse, JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework import permissions
from rest_framework import generics
from rest_framework import status

from user.models import User

from message.models import Message
from message.serializers import MessageSerializer

@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def message_detail(request, pk):
    # Função responsável por recuperar ou atualizar mensagem de id = pk

    try:
        message = Message.objects.get(pk=pk)
    except:
        content = {'error': 'Message not found.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

    # caso a requisição seja do tipo GET, retorna a mensagem para o cliente
    if request.method == 'GET':
        # Serializa o objeto mensagem para json, antes de o enviar ao cliente
        serialized_message = MessageSerializer(message).data
        return Response(serialized_message, status=status.HTTP_200_OK)

    # a mensagem é do tipo PUT, a requisição é para atualizar seu estado
    else:
        if type(request.data) == QueryDict:
            # Corrige valores de campos do dicionário vindos como lista (ocorre na biblioteca requests do python)
            data = request.data.dict()

        else:
            data = request.data

        # verifica se a requisição recebida informa que a mensagem foi lida, atualizando o estado da mensagem
        if data.get('read'):
            if not message.received_at:
                message.received_at = datetime.now()

            message.read_at = datetime.now()
            message.save()

            # TODO: Notificar ao usuário que enviou a mensagem que seu estado foi atualizado para "lida"

            # transforma a instância de mensagem em json
            serialized_message = MessageSerializer(message).data
            return Response(serialized_message, status=status.HTTP_200_OK)

        # verifica se a requisição informa que a mensagem foi recebida
        elif data.get('received'):
            message.received_at = datetime.now()
            message.save()

            # TODO: Notificar quem enviou a mensagem que ela foi recebida

            # transforma a instância de mensagem em json
            serialized_message = MessageSerializer(message).data
            return Response(serialized_message, status=status.HTTP_200_OK)

        # Mensagens só podem ser atualizadas para "recebida" ou "lida"
        else:
            content = {
                'error': 'Use this only to update message status for received or read.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_message(request):
    # Cria uma nova instância dde mensagem no banco de dados. Apenas usuários autenticados e requisições POST
    if type(request.data) == QueryDict:
        # Corrige valores de campos do dicionário vindos como lista (ocorre na biblioteca requests do python)
        data = request.data.dict()

    else:
        data = request.data

    # sequencia de verificações para validar mensagens
    # TODO: Validar mensagem em função específica

    # verifica se o destino da mensagem é válido
    receiver_username = data.get('username')
    if not receiver_username:
        content = {'error': 'username is required.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # verifica se o usuário destino da mensagem existe
    try:
        receiver = User.objects.get(username=receiver_username)

    except Exception as e:
        print(e)

        content = {'error': f'"{receiver_username}" not found.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

    # verificia se o usuário que enviou a mensagem é o mesmo de destino
    if request.user == receiver:
        content = {'error': f'You cannot send messages to yourself.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # verifica se o conteúdo da mensagem é vazio
    message_content = data.get('message')
    if not message_content or not len(message_content):
        content = {'error': f'Empty message is not valid.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # Fim de sequencia de verificação de validade de mensagens
    
    else:
        try:
            # Tenta criar uma nova instância de mensagem
            message = Message.objects.create(
                        sender=request.user,
                        receiver=receiver,
                        content=message_content
                    )

            message.save()

            content = {'created_id': message.id}
            return Response(content, status=status.HTTP_201_CREATED)

        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
