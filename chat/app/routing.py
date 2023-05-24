# chat/routing.py

from django.urls import re_path,path
from .consumers import ChatConsumer, CallConsumer

websocket_urlpatterns = [

    path('ws/message/<str:username>/', CallConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<id>\d+)/$', ChatConsumer.as_asgi()),
]
