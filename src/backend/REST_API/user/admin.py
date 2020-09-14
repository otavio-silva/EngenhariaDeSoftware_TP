from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ('username', 'online', 'ip_address', 'email',
                    'first_name', 'last_name')
    ordering = ('username',)
