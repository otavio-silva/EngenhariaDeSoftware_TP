from django.urls import path
from api import views

urlpatterns = [
    path('messages/', views.message_list),
]
