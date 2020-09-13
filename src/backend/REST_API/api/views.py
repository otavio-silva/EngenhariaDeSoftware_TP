from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser

from chat.models import Chat
from message.models import Message

from message.serializers import MessageSerializer

def message_list(request):
    messages = Message.objects.all()
    serializer = MessageSerializer(messages, many=True)
    return JsonResponse(serializer.data, safe=False)