from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-j2ukx4$%nmn#*rti*07zw^q&c9ghshsvhbnf+dngkdi%bs7k$^'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
