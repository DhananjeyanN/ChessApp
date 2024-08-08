from django.urls import path
from accounts.views import home
from . import views

urlpatterns = [
    path('play_game/', views.play_game, name='play_game'),
    path('move/', views.make_move, name='move'),
    path('game_page/<int:id>', views.index, name='index'),
    path('join_game/', views.join_game, name='queue'),
    path('leave_queue/', views.remove_user_from_queue, name='leave_queue'),
    path('check_status/', views.check_status, name='check_status'),
    path('', home, name='pieces_home')
    # path('check/<str:color>/', views.check, name='check')
]