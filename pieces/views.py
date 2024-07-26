from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .gamelogic import Game
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import GamePlay, Player
from .serializers import MoveSerializer

# Create your views here.
@csrf_exempt
@api_view(['POST'])
def play_game(request):
    game = Game()
    if request.method == "POST":
        game = Game()
        game.board.initialize_board()
        gameplay = GamePlay()
        gameplay.save_game(game=game)
        return Response({'status':'Success', 'gameplay_id':gameplay.id}, status=200)

@csrf_exempt
@api_view(['POST'])
def make_move(request):
    serializer = MoveSerializer(data=request.data)
    if serializer.is_valid():
        source=tuple(serializer.validated_data['source'])
        dest=tuple(serializer.validated_data['dest'])
        gameplay = GamePlay.objects.latest('id')
        game_instance = Game.deserialize(gameplay.game_state)
        if game_instance.move(source, dest):
            gameplay.save_game(game=game_instance)
            return Response({'status':'success'}, status=200)
        else:
            return Response({'status':'fail'}, status=400)
    return Response(serializer.errors,status=400)


@api_view(['GET'])
def check_game_state(request):
    pass


def index(request):
    return render(request, 'index.html')