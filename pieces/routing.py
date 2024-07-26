from django.urls import path
from consumers import ChessConsumer
websocket_urlpatterns = [
    path('ws/game/<str:game_id>', ChessConsumer.as_asgi())
]