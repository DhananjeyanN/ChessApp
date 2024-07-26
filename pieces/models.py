from django.db import models
from accounts.models import User

from accounts.models import Profile
from pieces.gamelogic import Game


class Player(models.Model):
    name = models.CharField(max_length=120)
    is_white = models.BooleanField(default=False)

    def __str__(self):
        return self.name + 'Playing as' + 'white' if self.is_white else 'black'


class GamePlay(models.Model):
    game_state = models.TextField()
    white_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='white')
    black_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='black')

    def save_game(self, game):
        self.game_state = game.serialize()
        self.save()

    def load_game(self):
        return Game.deserialize(data=self.game_state)

    def __str__(self):
        return f'White: {self.white_player}, Black: {self.black_player}, Game State: {self.game_state}'

