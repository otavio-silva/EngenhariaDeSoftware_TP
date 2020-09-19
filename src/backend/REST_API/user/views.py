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

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_detail(request, username):
    #Recupera um usuário por seu username. 
    # - As requisições devem ser do tipo GET e serem feitas de usuários autenticados.

    try:
        user = User.objects.get(username=username)
    except:
        content = {'error': f'"{username}" not found.'}
        return JsonResponse(content, status.HTTP_404_NOT_FOUND)

    user.update_online_status()

    serialized_user = UserSerializer(user).data
    return JsonResponse(serialized_user, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def user_keep_active(request):
    '''Mantém o estado do usuário como ativo.

    O usuário deve mandar requisições períodicas para este local indicando que está ativo.
    '''

    try:
        user = request.user 

        now = datetime.now()
        ip_address = request.META['REMOTE_ADDR']

        user.set_ip_address(ip_address)
        user.set_last_live_signal(now)

        user.save()

        return Response(status=status.HTTP_200_OK)

    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_user(request):
    # Cria um usuário por meio de requisições tipo POST

    # requesta.data é um dicionário que armazena os dados de criação do usuário
    if type(request.data) == QueryDict:
        # Corrige valores de campos do dicionário vindos como lista (ocorre na biblioteca requests do python)
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
