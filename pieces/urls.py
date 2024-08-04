from django.urls import path

from . import views

urlpatterns = [
    path('play_game/', views.play_game, name='play_game'),
    path('move/', views.make_move, name='move'),
    path('game_page/<int:id>', views.index, name='index'),
    path('queue', views.join_queue, name='queue'),
    path('leave_queue', views.remove_user_from_queue, name='leave_queue'),
    path('create_game', views.create_game, name='create_game'),
    # path('check/<str:color>/', views.check, name='check')
]