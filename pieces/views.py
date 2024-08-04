from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .gamelogic import Game
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.forms import AddUserToQueueForm
from .models import GamePlay, Player, UserQueue
from .serializers import MoveSerializer
from .utils import reorder_queue


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

@api_view(['POST', 'GET'])
def join_queue(request):
    if request.method == 'POST':
        if not UserQueue.objects.filter(user=request.user).exists():
            user_queue = UserQueue(user=request.user)
            user_queue.position = UserQueue.objects.count()+1
            user_queue.save()
        return redirect('home')
    else:
        queue = UserQueue.objects.all().order_by('position')
        user_queue = UserQueue.objects.filter(user=request.user)
        if user_queue:
            user_queue = user_queue[0]

        return render(request, 'home.html', context={'queue':queue, 'user_queue':user_queue, 'gameplay_id':create_game()})

def remove_user_from_queue(request):
    user_queue = UserQueue.objects.filter(user = request.user)[0]
    user_queue.delete()
    reorder_queue()
    return redirect('home')


def create_game():
    if len(UserQueue.objects.all()) >=2:
        p1 = UserQueue.objects.filter(position=1)[0]
        p2 = UserQueue.objects.filter(position=2)[0]
        UserQueue.objects.filter(position=1).delete()
        UserQueue.objects.filter(position=2).delete()
        reorder_queue()
        gameplay = GamePlay()
        gameplay.white_player = p1
        gameplay.black_player = p2
        game = Game()
        game.board.initialize_board()
        gameplay.save_game(game)
        print(gameplay.id)
        return gameplay.id
    else:
        return -1
