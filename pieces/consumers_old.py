import json

from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from .models import GamePlay
from gamelogic import Game
from .views import gameplay


class ChessConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_group_name = f'game_{self.game_id}'
        await self.channel_layer.group_add(self.game_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.game_group_name, self.channel_name)

    async def recieve(self, text_data):
        text_data_json = json.loads(text_data)
        source = text_data_json['source']
        dest = text_data_json['dest']
        game = self.get_game()
        game_instance = Game.deserialize(game.game_state)
        if game_instance.move(source=source,dest=dest):
            game.game_state = game_instance.serialize()
            await game.save_game()
            await self.channel_layer.group_send(
                self.game_group_name, {
                    'type':'move_made',
                    'source':source,
                    'dest':dest
                }
            )
        else:
            await self.send(text_data=json.dumps({
                'status':'failed....'
            }))

    async def get_game(self):
        return await database_sync_to_async(gameplay.objects.get)(id=self.game_id)

    async def move_made(self, event):
        source = event['source']
        dest = event['dest']
        await self.send(text_data=json.dumps({
            'source':source,
            'dest':dest
        }))

    async def save_game(self, game):
        await database_sync_to_async(game.save)()