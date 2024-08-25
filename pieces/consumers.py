import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import GamePlay
from .gamelogic import Game

class ChessConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_group_name = f'game_{self.game_id}'
        await self.channel_layer.group_add(self.game_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.game_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        source = text_data_json['source']
        dest = text_data_json['dest']

        # Process move in the game state
        game = await sync_to_async(GamePlay.objects.get)(id=self.game_id)
        game_instance = Game.deserialize(game.game_state)

        if game_instance.move(source=source, dest=dest):
            await sync_to_async(game.save_game)(game_instance)

            # Send move to group
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'move_made',
                    'source': source,
                    'dest': dest,
                }
            )
        else:
            await self.send(text_data=json.dumps({
                'status': 'failed'
            }))

    async def move_made(self, event):
        source = event['source']
        dest = event['dest']

        # Send move to WebSocket
        await self.send(text_data=json.dumps({
            'source': source,
            'dest': dest,
        }))