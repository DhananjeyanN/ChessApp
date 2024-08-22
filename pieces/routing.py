from django.urls import path, re_path
from consumers import ChessConsumer
from pieces import consumers

websocket_urlpatterns = [
    path('ws/chess/<str:game_id>/', ChessConsumer.as_asgi()),
]