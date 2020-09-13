from rest_framework import serializers
from message.models import Message

class MessageSerializer(serializers.ModelSerializer):
    chat = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    sender = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Message
        fields = ['pk', 'chat', 'sender', 'content', 'sent_at', 'received_at', 'read_at']