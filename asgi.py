# asgi.py
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from messaging import consumers

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GINFO.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        path("ws/chat/<int:receiver_id>/", consumers.ChatConsumer.as_asgi()),
    ]),
})