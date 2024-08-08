from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .gamelogic import Game
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.forms import AddUserToQueueForm
from .models import GamePlay, Player, UserQueue
from .serializers import MoveSerializer
from .utils import reorder_queue

gameplay = None

# Create your views here.
@csrf_exempt
@api_view(['POST'])
def play_game(request):
    if request.method == "POST":
        game = Game()
        game.board.initialize_board()
        wp = Player.objects.get(name='player_1')
        bp = Player.objects.get(name='player_2')
        gameplay = GamePlay(white_player=wp, black_player=bp)
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
        game_instance.board.print_board()
        print(source, dest, 'GHGHGHGHGHGHGHGHGHGHHHHHHHHH')
        if game_instance.move(source, dest):
            gameplay.save_game(game=game_instance)
            game_instance.board.print_board()
            return Response({'status':'success'}, status=200)
        else:
            return Response({'status':'fail'}, status=400)
    return Response(serializer.errors,status=400)


@api_view(['GET'])
def check_game_state(request):
    pass


def index(request):
    return render(request, 'index.html')

@login_required
@api_view(['POST'])
@csrf_exempt
def join_game(request):
    user=request.user
    gameplay = GamePlay.objects.filter(is_ready=False).first()
    if gameplay and gameplay.white_player and not gameplay.black_player:
        gameplay.black_player = Player.objects.create(user=user, is_white = False)
        gameplay.is_ready = True
        gameplay.save()
        return JsonResponse({'status':'joined_game','gameplay_id':gameplay.id},status=200)
    else:
        white_player = Player.objects.create(user=user,is_white=True)
        game = Game()
        game.board.initialize_board()
        new_gameplay = GamePlay()
        new_gameplay.white_player = white_player
        new_gameplay.save_game(game=game)
        new_gameplay.save()
        return JsonResponse({'status':'initialized_game','gameplay_id':gameplay.id}, status=200)

@login_required
@api_view(['POST'])
@csrf_exempt
def check_status(request):
    gameplay_id = request.data.get('gameplay_id')
    gameplay = GamePlay.objects.get(id=gameplay_id)
    return JsonResponse({'is_ready':gameplay.is_ready}, status=200)




def remove_user_from_queue(request):
    global p1
    if p1 == Player.objects.filter(user=request.user):
        p1 = None
    return redirect('home')


