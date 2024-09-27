from django.urls import path
from .consumers import FtWebsocket

websocket_urlpatterns = [
    path("ws", FtWebsocket.as_asgi()),
    # path("wss/", FtWebsocket.as_asgi()),
]
