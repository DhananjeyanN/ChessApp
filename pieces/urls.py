from django.urls import path
from . import views

urlpatterns = [
    path('play_game/', views.play_game, name='play_game'),
    path('move/', views.make_move, name='move'),
    path('promote/', views.promote, name='promote'),
    path('game_page/<int:game_id>', views.index, name='index'),
    path('game_page/get_game_state/<int:game_id>', views.get_game_state, name='get_game_state'),
    path('join_game/', views.join_game, name='queue'),
    path('user_game_state/', views.user_game_state, name='user_game_state'),
    path('close_game/', views.close_game, name='close_game'),
    path('leave_queue/', views.remove_user_from_queue, name='leave_queue'),
    path('check_status/', views.check_status, name='check_status'),
    path('get_messages/', views.get_messages, name='get_messages'),
    path('', views.home, name='home')
    # path('check/<str:color>/', views.check, name='check')
]