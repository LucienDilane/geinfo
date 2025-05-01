# asgi.py
import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

# Importe tes consumers ici (nous allons les créer ensuite)
# from . import consumers

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GINFO.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        # Ici, tu définiras les URLs pour tes consumers WebSocket
        # path("ws/chat/<room_name>/", consumers.ChatConsumer.as_asgi()),
    ]),
})