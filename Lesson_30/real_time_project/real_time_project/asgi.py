"""
ASGI config for real_time_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

import chat.routing
import counter.routing
import notifications.routing
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'real_time_project.settings')

django_app = get_asgi_application()

application = ProtocolTypeRouter({
	"http": django_app,
	"websocket": AuthMiddlewareStack(
		URLRouter(counter.routing.websocket_urlpatterns +
		          notifications.routing.websocket_urlpatterns +
		          chat.routing.websocket_urlpatterns)
	),
})
