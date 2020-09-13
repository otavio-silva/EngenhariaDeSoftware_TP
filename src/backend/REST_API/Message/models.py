from django.db import models
from django.contrib.auth.models import User

from Chat.models import Chat

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)

    content = models.TextField('Content', max_length=1024)

    sent_at = models.DateTimeField('Sent at', auto_now_add=True)
    received_at = models.DateTimeField('Received at', null=True, blank=True)
    read_at = models.DateTimeField('Read at', null=True, blank=True)
