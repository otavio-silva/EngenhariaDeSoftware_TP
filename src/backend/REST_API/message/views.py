from datetime import datetime

from django.http import HttpResponse, JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework import permissions
from rest_framework import generics
from rest_framework import status

from user.models import User
from message.models import Message
from api.serializers import MessageSerializer

@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def message_detail(request, pk):
    try:
        message = Message.objects.get(pk=pk)
    except:
        content = {'error': 'Message not found.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serialized_message = MessageSerializer(message).data
        return Response(serialized_message, status=status.HTTP_200_OK)

    else:
        data = request.data
        
        if data.get('read'):
            if not message.received_at:
                message.received_at = datetime.now()
            
            message.read_at = datetime.now()
            message.save()

            serialized_message = MessageSerializer(message).data
            return Response(serialized_message, status=status.HTTP_200_OK)

        elif data.get('received'):
            message.received_at = datetime.now()
            message.save()

            serialized_message = MessageSerializer(message).data
            return Response(serialized_message, status=status.HTTP_200_OK)

        else:
            content = {
                'error': 'Use this only to update message status for received or read.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_message(request):
    data = request.data     

    receiver_username = data.get('username')
    if not receiver_username:
        content = {'error': 'username is required.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    try:    
        receiver = User.objects.get(username=receiver_username)

    except:
        content = {'error': f'"{receiver_username}" not found.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

    if request.user == receiver:
        content = {'error': f'You cannot send messages to yourself.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    message_content = data.get('message')
    if not message_content or not len(message_content):
        content = {'error': f'Empty message is not valid.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    else:
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
