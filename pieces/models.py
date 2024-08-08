from django.db import models
from accounts.models import User

from accounts.models import Player
from pieces.gamelogic import Game

class GamePlay(models.Model):
    game_state = models.TextField()
    white_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='white')
    black_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='black')
    is_ready = models.BooleanField(default=False)

    def save_game(self, game):
        self.game_state = game.serialize()
        self.save()

    def load_game(self):
        return Game.deserialize(data=self.game_state)

    def __str__(self):
        return f'White: {self.white_player}, Black: {self.black_player}, Game State: {self.game_state}'

class UserQueue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()

    def __str__(self):
        return f'Username: {self.user.username}, Position: {self.position}'

