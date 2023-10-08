from django.urls import path, include, re_path
from messenger.consumers import ChatConsumer

websocket_urlpatterns = [
    #path("<room_slug>", ChatConsumer.as_asgi()),
    #re_path(r'^ws/(?P<room_slug>[^/]+)/$', ChatConsumer.as_asgi()),
    path("<room_name>", ChatConsumer.as_asgi()),
    re_path(r'^ws/(?P<room_slug>[^/]+)/$', ChatConsumer.as_asgi()),
]