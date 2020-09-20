from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.http.request import QueryDict

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework import permissions
from rest_framework import generics
from rest_framework import status

from rest_framework.authtoken.models import Token

from user.models import User
from user.serializers import UserSerializer

from root.views import check_message

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_detail(request, username):
    ''' Recupera um usuário no banco de dados pelo seu `username`.

    É necessário que o usuário que fez a requisição esteja autenticado e utilize o método GET.

    Args:
        request: Requisição HTTP do tipo GET
        username: `username` do usuário a ser recuperado no banco de dados.

    Returns:
        Json com informações sobre usuário de `username` ou que ele não existe.

    '''

    try:
        user = User.objects.get(username=username)

    except:
        content = {'error': f'"{username}" not found.'}
        return JsonResponse(content, status.HTTP_404_NOT_FOUND)

    # Verifica se o usuário está online ou não, atualizando o campo `online` de acordo antes de enviar
    # a resposta ao front
    user.update_online_status()

    serialized_user = UserSerializer(user).data
    return JsonResponse(serialized_user, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def user_keep_active(request):
    '''Mantém o estado do usuário como ativo.

    O usuário deve mandar requisições períodicas para este local indicando que está ativo.

    Args:
        request: Requisição HTTP do tipo PUT.

    Returns:
        Código HTTP 200 indicando que a requisição do usuário ocorreu sem erros ou 500, se houve algum erro
    '''

    try:
        user = request.user

        now = datetime.now()
        ip_address = request.META['REMOTE_ADDR']  # endereço ip do usuário

        user.set_ip_address(ip_address)
        user.set_last_active_signal(now)
        user.save()

        # Checa se o usuario ativo possui alguma mensagem que ainda nao foi recebida
        # Caso possua, promove o recebimento delas
        check_message(request)

        return Response(status=status.HTTP_200_OK)

    except:
       return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_user(request):
    ''' Recebe requisições do tipo POST com dados para criação de um novo usuário

    Args:
        request: Requisição HTTP do tipo POST.

    Returns:
        Json com informações do usuário criado e código HTTP 201 confirmando a criação do mesmo
        ou json com erro e código HTTP 400, caso houve algum erro
    '''

    # requesta.data é um dicionário que armazena os dados de criação do usuário
    # A condição abaixo corrige valores de campos do dicionário vindos como lista (ocorre na biblioteca requests do python)
    if type(request.data) == QueryDict:
        data = request.data.dict()

    else:
        data = request.data

    try:
        # TODO: Validar os dados enviados antes de criar usuário
        user = User.objects.create(**data)
        user.set_password(data['password'])
        user.save()

        # criação de token de autenticação do usuário
        Token.objects.create(user=user)

        serialized_user = UserSerializer(user).data
        return JsonResponse(serialized_user, status=status.HTTP_201_CREATED)

    except Exception as e:
        content = {'error': str(e)}
        return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)
