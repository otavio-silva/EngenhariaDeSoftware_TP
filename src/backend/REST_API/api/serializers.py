from user.models import User

from rest_framework import serializers
from message.models import Message

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User 
        fields = ['online', 'first_name', 'last_name', 'username', 'password']
    
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        
        return user

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    receiver = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver' , 'content',
                  'created_at', 'received_at', 'read_at']
