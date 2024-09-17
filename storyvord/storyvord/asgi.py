"""
ASGI config for storyvord project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from inbox.routing import websocket_urlpatterns as inbox_urlpatterns
from ai_assistant.routing import websocket_ai_chat_urlpatterns
from channels.security.websocket import AllowedHostsOriginValidator
import django
django.setup()

from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storyvord.settings')
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
        URLRouter(
                 inbox_urlpatterns + websocket_ai_chat_urlpatterns
                )
    ),
    )
    }
)
