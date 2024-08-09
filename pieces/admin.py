from django.contrib import admin

from pieces.models import GamePlay, Player, UserQueue

# Register your models here.
admin.site.register(Player)
admin.site.register(UserQueue)

class GamePlayAdmin(admin.ModelAdmin):
    list_display = ('id',)
admin.site.register(GamePlay, GamePlayAdmin)