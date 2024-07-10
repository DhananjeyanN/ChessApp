from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MoveSerializer

# Create your views here.
game = Game()
@api_view(['POST'])
def play_game(request):
    global game
    game.board.initialize_board()
    print('BBBBBBBB')
    game.turn = 'white'
    return Response({'status':'Success'}, status=200)

@api_view(['POST'])
def make_move(request):
    global game
    serializer = MoveSerializer(data=request.data)
    if serializer.is_valid():
        source = tuple(serializer.validated_data['source'])
        dest = tuple(serializer.validated_data['dest'])
        print(source, dest, 'SOURCE-DEST')
        game.board.print_board()
        is_valid = game.move(source=source, dest=dest)
        print(is_valid, 'ISVALID')
        if is_valid:
            return Response({'status':'Success'}, status=200)
        else:
            return Response({'status':'Failed'}, status=400)
    return Response(serializer.errors, status=400)
@api_view(['GET'])
def check_game_state(request):
    pass


def index(request):
    return render(request, 'index.html')