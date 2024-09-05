from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .gamelogic import Game
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import GamePlay, Player
from .serializers import MoveSerializer


@csrf_exempt
@api_view(['POST'])
@login_required
def play_game(request):
    if request.method == "POST":
        game = Game()
        game.board.initialize_board()
        wp = Player.objects.get(name='player_1')
        bp = Player.objects.get(name='player_2')
        gameplay = GamePlay(white_player=wp, black_player=bp)
        gameplay.save_game(game=game)
        return Response({'status': 'Success', 'gameplay_id': gameplay.id}, status=200)


@login_required()
def get_game_state(request, game_id):
    gameplay = get_object_or_404(GamePlay, id=game_id)
    return JsonResponse({'status':'success', 'game_state':gameplay.game_state})

@login_required()
@csrf_exempt
@api_view(['POST'])
def get_messages(request):
    player = Player.objects.filter(user=request.user)[0]
    gameplay_id = request.data['gameplay_id']
    print(gameplay_id, 'GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG')
    gameplay = get_object_or_404(GamePlay, id=gameplay_id)
    if player == gameplay.white_player:
        color = 'white'
    else:
        color = 'black'
    w_in_check = gameplay.white_player_in_check
    w_is_winner = gameplay.white_player_is_winner
    b_in_check = gameplay.black_player_in_check
    b_is_winner = gameplay.black_player_is_winner
    print(b_in_check)

    return JsonResponse({'status':'success', 'w_in_check':w_in_check, 'w_is_winner':w_is_winner, 'b_in_check':b_in_check, 'b_is_winner':b_is_winner, 'color':color})


@login_required()
@csrf_exempt
@api_view(['POST'])
def make_move(request):
    serializer = MoveSerializer(data=request.data)
    if serializer.is_valid():
        current_player = Player.objects.filter(user=request.user)[0]
        source = tuple(serializer.validated_data['source'])
        dest = tuple(serializer.validated_data['dest'])
        gameplay_id = int(request.data['gameplay_id'])
        gameplay = get_object_or_404(GamePlay, id=gameplay_id)
        game_instance = gameplay.load_game()
        piece_color = game_instance.board.board[source[0]][source[1]].get_piece().get_color()
        w_p = gameplay.white_player
        b_p = gameplay.black_player
        if current_player == w_p:
            current_player_color = 'white'
        else:
            current_player_color = 'black'
        if current_player_color == piece_color:
            if game_instance.move(source, dest):
                gameplay.save_game(game=game_instance)
                game_instance.board.print_board()
                if game_instance.checkmate:
                    if game_instance.turn == 'white':
                        gameplay.white_player_is_winner = True
                        gameplay.save()
                    else:
                        gameplay.black_player_is_winner = True
                        gameplay.save()
                    gameplay.completed = True
                    gameplay.save()
                print('CHECCCKKKK',game_instance.check)
                if game_instance.check:
                    print('SOMEONE IN CHECK')
                    if game_instance.turn == 'white':
                        gameplay.white_player_in_check = True
                        gameplay.save()
                    else:
                        gameplay.black_player_in_check = True
                        gameplay.save()
                else:
                    gameplay.white_player_in_check = False
                    gameplay.black_player_in_check = False
                    gameplay.save()
                return Response({'status': 'success'}, status=200)
            else:
                return Response({'status': 'fail'}, status=400)
        else:
            return Response({'status': 'fail'}, status=400)
    return Response(serializer.errors, status=400)


def index(request, game_id):
    gameplay = GamePlay.objects.get(id=game_id)
    player = Player.objects.filter(user=request.user)
    print(player)
    is_white = False
    if gameplay.white_player == player[0]:
        is_white = True
    print(is_white, 'IS_WHITE')
    return render(request, 'index.html', context={'gameplay': gameplay, 'gameplay_id':game_id, 'is_white':is_white})


@login_required
@api_view(['POST'])
@csrf_exempt
def join_game(request):
    player = get_object_or_404(Player, user=request.user)
    open_game = GamePlay.objects.filter(black_player = None)
    prev_game_as_b = GamePlay.objects.filter(black_player = player, completed=False)
    prev_game_as_w = GamePlay.objects.filter(white_player = player, completed=False)
    if prev_game_as_b:
        return JsonResponse({'status': 'previous_game_found', 'gameplay_id': prev_game_as_b[0].id}, status=200)
    elif prev_game_as_w:
        return JsonResponse({'status': 'previous_game_found', 'gameplay_id': prev_game_as_w[0].id}, status=200)
    if open_game:
        open_game = open_game[0]
        open_game.black_player = player
        open_game.is_ready = True
        open_game.save()
        return JsonResponse({'status': 'joined_game', 'gameplay_id': open_game.id}, status=200)
    else:
        game = Game()
        game.board.initialize_board()
        gameplay = GamePlay()
        gameplay.white_player = player
        gameplay.save_game(game=game)
        gameplay.save()
        return JsonResponse({'status': 'initialized_game', 'gameplay_id': gameplay.id}, status=200)


@login_required
@api_view(['POST'])
@csrf_exempt
def check_status(request):
    gameplay_id = request.data.get('gameplay_id')
    gameplay = GamePlay.objects.get(id=gameplay_id)
    return JsonResponse({'is_ready': gameplay.is_ready}, status=200)


@login_required()
@api_view(['POST'])
@csrf_exempt
def user_game_state(request):
    player = Player.objects.get(user=request.user)
    white_p_game = None
    black_p_game = None

    if GamePlay.objects.filter(completed=False, white_player=player):
        white_p_game = GamePlay.objects.filter(completed=False, white_player=player)[0]

    if GamePlay.objects.filter(completed=False, black_player=player):
        black_p_game = GamePlay.objects.filter(completed=False, black_player=player)[0]

    if white_p_game:
        if white_p_game.black_player is None:
            return JsonResponse({'status': 'loading', 'gameplay_id': white_p_game.id})
        else:
            return JsonResponse({'status': 'game_in_progess', 'gameplay_id': white_p_game.id})
    elif black_p_game:
        return JsonResponse({'status': 'game_in_progess', 'gameplay_id': black_p_game.id})
    else:
        return JsonResponse({'status': 'no_game'})


@login_required()
@api_view(['POST'])
@csrf_exempt
def remove_user_from_queue(request):
    game = GamePlay.objects.filter(white_player=Player.objects.get(user=request.user), is_ready=False)
    if game:
        game[0].delete()
        return JsonResponse({'status': 'deleted'}, status=200)
    else:
        return JsonResponse({'status': 'game_not_found'}, status=400)


@login_required()
@api_view(['POST'])
@csrf_exempt
def close_game(request):
    game_w = GamePlay.objects.filter(white_player=Player.objects.get(user=request.user), is_ready=True, completed = False)
    game_b = GamePlay.objects.filter(black_player=Player.objects.get(user=request.user), is_ready=True, completed = False)
    if game_w:
        game = game_w[0]
    elif game_b:
        game = game_b[0]
    print(game, game.completed,game.id, 'GAMEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
    game.completed = True
    game.save()
    print(game, game.completed,game.id, 'GAMEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
    return JsonResponse({'status': 'game_closed'}, status=200)


def home(request):
    game_exists = False
    gameplay_id = None
    if Player.objects.filter(user=request.user.id):
        player = Player.objects.filter(user=request.user.id)[0]
        gameplay = GamePlay.objects.filter(is_ready=False, white_player=player)
        if gameplay and len(gameplay) != 0:
            game_exists = True
            messages.warning(request, 'Game is Waiting for Opponent')
            gameplay_id = gameplay[0].id
    print(game_exists, gameplay_id)
    return render(request, 'home.html', context={'game_exists': game_exists})
