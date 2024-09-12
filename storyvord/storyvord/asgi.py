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
from inbox import routing
import ai_assistant.routing
from channels.security.websocket import AllowedHostsOriginValidator
import django
django.setup()

from django.urls import path
from ai_assistant.consumers import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storyvord.settings')
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                path("ws/chat/", ChatConsumer.as_asgi()),
            ]
        )
    ),
})
