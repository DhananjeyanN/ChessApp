from django.contrib import admin

from pieces.models import GamePlay, Player, UserQueue

# Register your models here.
admin.site.register(GamePlay)
admin.site.register(Player)
admin.site.register(UserQueue)