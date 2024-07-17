from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Game
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MoveSerializer

# Create your views here.
game = Game()
@csrf_exempt
@api_view(['POST'])
def play_game(request):
    global game
    game.board.initialize_board()
    game.board.print_board()
    game.checkmate = False
    game.check = False
    game.turn = 'white'
    return Response({'status':'Success'}, status=200)

@csrf_exempt
@api_view(['POST'])
def make_move(request):
    global game
    serializer = MoveSerializer(data=request.data)
    if serializer.is_valid():
        source = tuple(serializer.validated_data['source'])
        dest = tuple(serializer.validated_data['dest'])
        print(source, dest, 'SOURCE-DEST')
        game.board.print_board()
        print(source, dest)
        is_valid = game.move(source, dest)
        print(is_valid, 'ISVALID')
        print(game.turn, game.check, game.checkmate)
        if is_valid:
            print('CHECK', game.check, 'CHECKMATE', game.checkmate)
            if game.turn == 'white':
                check_color = 'black'
            else:
                check_color = 'white'
            return Response({'status':'Success', 'check':game.check, 'checkmate':game.checkmate, 'checked_king':check_color, 'winner':game.turn}, status=200)
        else:
            return Response({'status':'Failed'}, status=400)
    return Response(serializer.errors, status=400)
@api_view(['GET'])
def check_game_state(request):
    pass


def index(request):
    return render(request, 'index.html')