from django.urls import path
from . import views


urlpatterns = [
   path('', views.main_page, name="main_page"),
   path('6-handshakes', views.handshake, name="handshake"),
]
