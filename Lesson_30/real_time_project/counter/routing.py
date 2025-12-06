from django.urls import path

from .consumers import OnlineCounterConsumer

websocket_urlpatterns = [
	path("ws/online-counter/", OnlineCounterConsumer.as_asgi()),
]
