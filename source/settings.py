import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '^5b8p7m5j5*w9b=@9g3p4ixy=3!ycpw-ruf0#xj%v)!0cj4h2e'
DEBUG = True


ALLOWED_HOSTS = []
LigdiCash_API_Key ="MAGPMLT3QFJLIPUDN"
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZF9hcHAiOjE1MDA5LCJpZF9hYm9ubmUiOjg5OTQyLCJkYXRlY3JlYXRpb25fYXBwIjoiMjAyNC0wNC0wOCAwODozMjoyNCJ9.NRcyHfFO8OyaXOaklZ2DJ2Arf-gV8OXGfMIELQzdw88"

INSTALLED_APPS = [
    'crispy_forms',
    'registration',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
  
    'users',
    'courses',
    'evaluer',
    'choix'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'source.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'source.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
STATIC_ROOT = os.path.join(BASE_DIR,'static')
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "users/static_in_users", "static_files"),
]

CRISPY_TEMPLATE_PACK = 'bootstrap3'

ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True

REGISTRATION_OPEN = True

LOGIN_REDIRECT_URL = '/courses'
LOGIN_URL = '/accounts/login'

SITE_ID = 1

settings_sensitive = BASE_DIR + '/source/settings_sensitive.py'
if os.path.isfile(settings_sensitive):
    from settings_sensitive import *









DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'mohamedyakeri@gmail.com'
EMAIL_HOST_PASSWORD = 'lhye file icun oaqm'
AUTH_USER_MODEL = 'users.UserProfile'
