import os.path
from pathlib import Path

SECRET_KEY = 'django-insecure-n7e%29sf9sbasv@)mvsdfdsfafnjdsaNJDKLasd1ny+!@l-sbc*3gct(*6lomaj4by#1r5'

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
