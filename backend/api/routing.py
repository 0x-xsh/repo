from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from .consumers import NotificationConsumer

websocket_urlpatterns = [
    path(r"ws/notifications/<int:id>", NotificationConsumer.as_asgi()),
]

