from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    # Template padrão para que seja possível extender a classe User 
 
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError(_('The given username must be set'))
    
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
    
        user.set_password(password)
        user.save(using=self._db)
    
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    # Adiciona novos campos a classe User
    
    # se false, o usuário está offline
    online = models.BooleanField('Online', default=False, help_text='Online/offline')
    ip_address = models.CharField(
        'IP Address', max_length=12, default='127.0.0.1')

    last_live_signal = models.DateTimeField('Last live signal', auto_now_add=True) 

    objects = UserManager()