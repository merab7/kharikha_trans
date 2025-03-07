from pathlib import Path
import os
from django.utils.translation import gettext_lazy as _
import dj_database_url
import environ

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
env = environ.Env()
environ.Env.read_env()
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=True)




ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'kharikhatrans-production.up.railway.app',
    'jerseys.ge',
    'www.jerseys.ge',
]

CSRF_TRUSTED_ORIGINS = ['https://kharikhatrans-production.up.railway.app', 'https://jerseys.ge', 'https://www.jerseys.ge', ]

# application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
    'card',
    'customers',
    'crispy_forms',
    "crispy_bootstrap4",
    "payment",
    'django.contrib.sitemaps',
    'sitemap_generate',
]

SITEMAP_MAPPING = 'store.urls.sitemaps'
SITEMAP_INDEX_NAME = 'sitemap-index'
SITEMAPS_VIEW_NAME = 'django.contrib.sitemaps.views.sitemap'
SITEMAP_MEDIA_PATH = 'sitemaps'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'gecom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # customs
                'store.context_processors.category_names',
                'card.context_processors.cart',
                'store.context_processors.quantity_proc',
                ],
        },
    },
]

WSGI_APPLICATION = 'gecom.wsgi.application'


# database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


POSTGRES_LOCALLY=False
if env.bool('PRODUCTION') or POSTGRES_LOCALLY:
    DATABASES['default']= dj_database_url.parse(env('DATABASE_URL'))



# password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('en', 'English'),
    ('ka', 'Georgian'),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]


TIME_ZONE = 'UTC'




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
# Static files (CSS, JavaScript, images)
# STATIC_URL = '/static/'

# # The absolute path to the directory where collectstatic will collect static files for deployment.
# STATIC_ROOT = BASE_DIR / 'staticfiles'

# # Additional locations the staticfiles app will traverse if the FileSystemFinder finder is enabled.
# STATICFILES_DIRS = [
#     BASE_DIR / 'static',
# ]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files (user-uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# whiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"

CRISPY_TEMPLATE_PACK = "bootstrap4"

LOGIN_REDIRECT_URL = 'home'

#for to get user in the login page after non_login user tries to go profile 
#and after login they will go to the profile
LOGIN_URL = 'login'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#SMTP Parameters 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = env('EXCAVATIO')
EMAIL_HOST_PASSWORD = env('EMAIL_PASSWORD')
EMAIL_USE_TLS = True