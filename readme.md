pip install django
django-admin startproject chessapp .


import os.path
from pathlib import Path

SECRET_KEY = 'django-insecure-n7e%29sf9sbasv@)mvsdfdsfafnjdsaNJDKLasd1ny+!@l-sb>

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost','chessapp.me','www.chessapp.me']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'chess_db',
        'USER': 'dbadmin',
        'PASSWORD': 'Jicker1923',
        'HOST': 'localhost'
    }
}
Castling is a special move in chess involving the king and one of the rooks. It’s the only move in chess where two pieces (the king and a rook) are moved at the same time, and it is typically used to safeguard the king by moving it to a more protected position, while also activating the rook.

How Castling Works:

 • King-side Castling (Short Castling): The king moves two squares toward the rook on the king’s side, and the rook jumps over the king to land on the square next to the king.
 • Queen-side Castling (Long Castling): The king moves two squares toward the rook on the queen’s side, and the rook jumps over the king to land next to the king.



Conditions for Castling:



 1. Neither the king nor the rook involved has moved yet during the game.
 2. No pieces are between the king and the rook.
 3. The king is not in check, and the squares the king moves across, or the square it lands on, must not be under attack by an opponent’s piece.
 4. The king cannot move into check.
