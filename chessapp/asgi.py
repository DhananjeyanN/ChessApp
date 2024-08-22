"""
ASGI config for chessapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from pieces.routing import websocket_urlpatterns

import pieces.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chessapp.settings')

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(websocket_urlpatterns)
        )
    ),
})
