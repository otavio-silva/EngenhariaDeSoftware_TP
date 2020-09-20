from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    ''' Classe/template básico necessário para estender o modelo User do Django
    '''
    
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
    '''Adiciona novos campos e classe AbstractUser do Django 
    '''
    
    # se false, o usuário está offline
    online = models.BooleanField('Online', default=False, help_text='Online/offline')

    # endereço ip do usuário, útil para rotear mensagens a ele
    ip_address = models.CharField('IP Address', max_length=12, default='127.0.0.1')

    #porta do usuário
    port = models.PositiveIntegerField('Port', default=5000)

    # timestamp do último sinal enviado pelo usuário pelo front de que está ativo
    last_active_signal = models.DateTimeField('Last live signal', auto_now_add=True) 

    objects = UserManager()

    def update_online_status(self, delta = 5):
        '''Atualiza o estado de online/offline do usuário verificando se ele mandou sinal de que está ativo nos últimos `delta` segundos
        '''
        now = datetime.now().timestamp()
        
        if (now - self.last_active_signal.timestamp() > delta):
            self.online = False
        else:
            self.online = True 

        self.save()

    def set_ip_address(self, new_ip):
        '''Atualiza o endereço ip do usuário 

        Args:
            new_ip: Novo ip associado ao usuário
        Returns:
            None
        '''
        self.ip_address = new_ip 

    def set_port(self, port):
        '''Atualiza a porta do usuário
        Args:
            port: porta do usuário
        Returns:
            None
        '''
        self.port = port
        
    def set_last_active_signal(self, time_active_signal):
        '''Atualiza o último horário que o usuário mandou sinal de que está ativo

        Args:
            time_active_signal: timestamp do horário atual, quando o usuário mandou sinal de que está ativo.
        Returns:
            None
        '''
        self.last_active_signal = time_active_signal
