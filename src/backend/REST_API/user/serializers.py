from rest_framework import serializers
from user.models import User

class UserSerializer(serializers.ModelSerializer):
    ''' Classe responsável por receber uma instância de usuário e transformá-la em JSon
    '''

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'online', 'first_name', 'last_name', 'username', 'password']

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user
