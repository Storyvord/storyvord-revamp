"""
ASGI config for storyvord project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storyvord.settings')

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import inbox.routing
import ai_assistant.routing
from channels.security.websocket import AllowedHostsOriginValidator

import django
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
        URLRouter(
                inbox.routing.websocket_urlpatterns + ai_assistant.routing.websocket_urlpatterns
        )
    ),
    )
})