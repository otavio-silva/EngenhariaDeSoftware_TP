from datetime import datetime
from django.http.request import QueryDict

from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from user.models import User

from message.models import Message
from message.serializers import MessageSerializer

from root.views import notify_user_read

@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def message_detail(request, pk):
    '''Recebe requisições do tipo GET para recuperar uma mensagem, ou PUT, para atualizar seu estado.

    Caso a requisição seja do tipo PUT (para atualizar mensagem), os únicos estados que se pode alterar é se a mensagem foi lida
    ou recebida.

    Args:
        request: Requisição HTTP do tipo GET ou PUT, para recuperar ou atualizar uma mensagem, respectivamente.
        pk: Primary Key - chave primária da mensagem a ser recuperada ou alterada

    Returns:
        JSon com informações sobre a mensagem recuperada ou alterada, com código HTTP 200
        ou possíveis erros e seus respectivos código HTTP
    '''

    # verifica se a mensagem existe
    try:
        message = Message.objects.get(pk=pk)

    except:
        content = {'error': 'Message not found.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

    # caso a requisição seja do tipo GET, a retorna como JSon para o cliente que a requeriu
    if request.method == 'GET':

        #transforma a instância de mensagem em json
        serialized_message = MessageSerializer(message).data
        return Response(serialized_message, status=status.HTTP_200_OK)

    # A requisição é do tipo PUT
    else:

        # request.data é um dicionário que possui os dados a serem alterados da mensagem, o condicional abaixo
        # corrige valores de campos do dicionário vindos como lista (ocorre na biblioteca requests do python)
        if type(request.data) == QueryDict:
            data = request.data.dict()

        else:
            data = request.data

        # verifica se a requisição recebida é para atualizar o estado da mensagem para "read"
        if data.get('read'):
            # registra se a mensagem foi recebida, se necessário
            if not message.received_at:
                message.received_at = datetime.now()

            # registra o horário que a mensagem foi lida
            message.read_at = datetime.now()
            message.save()

            # Notifica ao usuário que enviou a mensagem que seu estado foi atualizado para "lida"
            notify_user_read(message.id)

            # transforma a instância de mensagem em json
            serialized_message = MessageSerializer(message).data
            return Response(serialized_message, status=status.HTTP_200_OK)

        # Mensagens só podem ser atualizadas para "received" ou "read"
        else:
            content = {'error': 'Use this only to update message status for received or read.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_message(request):
    '''Recebe uma requisição POST com dados para criar uma nova mensagem

    Args:
        request: Requisição HTTP do tipo POST com dados de criação de mensagem

    Returns:
        JSon com id da mensagem que foi criada ou de erros, com o respectivo código HTTP.

    '''

    # request.data é um dicionário que possui os dados de criação da mensagem, a condicional abaixo
    # corrige valores de campos do dicionário vindos como lista (ocorre na biblioteca requests do python)
    if type(request.data) == QueryDict:
        data = request.data.dict()

    else:
        data = request.data

    # TODO: Validar mensagem em função específica

    # verifica se o destino da mensagem é válido
    receiver_username = data.get('username')
    if not receiver_username:
        content = {'error': 'username is required.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # verifica se o usuário destino da mensagem existe
    try:
        receiver = User.objects.get(username=receiver_username)

    except:
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

    # Tenta criar uma nova instância de mensagem
    try:
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
