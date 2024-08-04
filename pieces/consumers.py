import json
from channels.generic.websocket import WebsocketConsumer
from .models import GamePlay
from gamelogic import Game

class ChessConsumer(WebsocketConsumer):
    def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_group_name = f'game_{self.game_id}'
        self.channel_layer.group_add(self.game_group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        self.channel_layer.group_discard(self.game_group_name, self.channel_name)

    def recieve(self, text_data):
        text_data_json = json.loads(text_data)
        source = text_data_json['source']
        dest = text_data_json['dest']
        game = GamePlay.objects.get(id=self.game_id)
        game_instance = Game.deserialize(game.game_state)
        if game_instance.move(source=source,dest=dest):
            game.game_state = game_instance.serialize()
            game.save_game()
            self.channel_layer.group_send(
                self.game_group_name, {
                    'type':'move_made',
                    'source':source,
                    'dest':dest
                }
            )
        else:
            self.send(text_data=json.dumps({
                'status':'failed....'
            }))

    def move_made(self, event):
        source = event['source']
        dest = event['dest']
        self.send(text_data=json.dumps({
            'source':source,
            'dest':dest
        }))