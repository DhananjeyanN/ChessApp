from django.urls import path, re_path
from consumers import ChessConsumer
from pieces import consumers

websocket_urlpatterns = [
    re_path(r'ws/game/(?P<game_id>\w+)/$',ChessConsumer.as_asgi())
]