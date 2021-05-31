from django.urls import path
from . import views


urlpatterns = [
   path('', views.index, name="index"),
   path('6-handshakes', views.handshake, name="handshake"),
   path('contacts', views.contacts, name="contacts"),
]
