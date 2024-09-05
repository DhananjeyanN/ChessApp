from django.db import models
from accounts.models import User

from accounts.models import Player
from pieces.gamelogic import Game

class GamePlay(models.Model):
    game_state = models.TextField()
    white_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='white',blank=True, null=True)
    black_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='black',blank=True, null=True)
    white_player_in_check = models.BooleanField(default=False)
    white_player_is_winner = models.BooleanField(default=False)
    black_player_in_check = models.BooleanField(default=False)
    black_player_is_winner = models.BooleanField(default=False)
    is_ready = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def save_game(self, game):
        self.game_state = game.serialize()
        print(self.game_state, 'SERIALIZED GAME')
        self.save()

    def load_game(self):
        print(Game.deserialize(data=self.game_state), 'DESERIALIZED')
        return Game.deserialize(data=self.game_state)

    def __str__(self):
        return f'White: {self.white_player}, Black: {self.black_player}, Game State: {self.game_state}, GamePlay ID: {self.id}'

