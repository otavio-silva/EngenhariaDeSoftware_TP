from rest_framework import serializers
from message.models import Message

class MessageSerializer(serializers.ModelSerializer):
    # Transforma objetos do tipo mensagem em json

    sender = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    receiver = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content',
                  'created_at', 'received_at', 'read_at']
