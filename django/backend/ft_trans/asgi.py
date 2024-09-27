"""
ASGI config for ft_trans project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddleware

# from channels.auth import AuthMiddlewareStack, AuthMiddleware
from accounts.middleware import CustomSessionMiddleware
from channels.sessions import CookieMiddleware

# from channels.sessions import CookieMiddleware, SessionMiddleware

# from channels.sessions import CookieMiddleware

# from ws.routing import routing
from ws.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ft_trans.settings")


def CustomAuthMiddlewareStack(inner):
    """
    AuthMiddlewareStackをカスタム品に変更
    残念ながら動かない(備忘録として残す)
    """
    return CookieMiddleware(CustomSessionMiddleware(AuthMiddleware(inner)))


# MiddleWareを改造したため、ユーザー認証が効かないので AuthMiddlewareStackは使わない
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": CookieMiddleware(
            # "websocket": AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)  # WebSocketのルーティング
        ),
    }
)
