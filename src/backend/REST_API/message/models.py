from django.db import models
from user.models import User

class Message(models.Model):
    ''' Classe responsável por representar uma mensagem trocada entre dois usuários válidos. 
    '''
    
    sender = models.ForeignKey(User, related_name='messages_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)

    content = models.TextField('Content', max_length=1024)

    created_at = models.DateTimeField('Created at', auto_now_add=True)
    received_at = models.DateTimeField('Received at', null=True, blank=True)
    read_at = models.DateTimeField('Read at', null=True, blank=True)

    def __str__(self):
        return f'Message "{self.content}" from {self.sender.username} to {self.receiver.username}'
