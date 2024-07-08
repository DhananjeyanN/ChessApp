from django.urls import path

from . import views

urlpatterns = [
    path('start_game/', views.play_game, name='start_game'),
    path('move/', views.make_move, name='move'),
    path('', views.index, name='index'),
    # path('check/<str:color>/', views.check, name='check')
]