from .base import *

try:
    from .dev import *
except:
    # Overrides base.py settings here
    DEBUG = False

    # For static folder
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

    # HTTPS SETTINGS
    SECURE_SSL_REDIRECT = False
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False

    #will be True when we have SSL certificate
    SECURE_SSL_REDIRECT = False

    # Maybes
    # HSST SETTINGS
    SECURE_HSTS_SECONDS = 31536000 # 1 year
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'pgdb',
            'PORT': '5432',
        }
    }