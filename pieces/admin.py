from django.contrib import admin

from pieces.models import GamePlay, Player

# Register your models here.
admin.site.register(Player)

class GamePlayAdmin(admin.ModelAdmin):
    list_display = ('id',)
admin.site.register(GamePlay, GamePlayAdmin)