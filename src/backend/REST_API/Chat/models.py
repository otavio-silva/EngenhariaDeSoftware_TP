from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    name = models.CharField('Chat Name', max_length=64, null=True, blank=True)
    users = models.ManyToManyField(User, related_name='chats')

    is_group = models.BooleanField('Is group', default=False)

    def __str__(self):
        return str(self.name)