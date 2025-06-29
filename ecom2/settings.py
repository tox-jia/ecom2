from multiprocessing.process import AuthenticationString
from pathlib import Path
import os
from dotenv import load_dotenv

import cloudinary
import cloudinary.uploader
import cloudinary.api

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load our environmental variables
load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '...'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-dev-secret")
DEBUG = os.getenv("DEBUG", "True") == "True"


# ------------------------------------------------
# [Database] .ENV to toggle online/local (railway + database)
# ------------------------------------------------
USE_ONLINE_DB = os.getenv("USE_ONLINE_DB", "True") == "True"

if USE_ONLINE_DB:
    ALLOWED_HOSTS = [
        'https://shamelesis.com',
        'shamelesis.com',
        'ecom2-production-2c2f.up.railway.app',
        'https://ecom2-production-2c2f.up.railway.app'
    ]

    CSRF_TRUSTED_ORIGINS = [
        'https://shamelesis.com',
        'https://ecom2-production-2c2f.up.railway.app'
    ]

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'railway',
            'USER': 'postgres',
            'PASSWORD': os.getenv("DB_PASSWORD"),  # Loaded from .env
            'HOST': 'shuttle.proxy.rlwy.net',
            'PORT': '18926',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }




# # ------------------------------------------------
# # [Database 1] online (railway + database)
# # ------------------------------------------------
# ## connected to railway and domain
# ALLOWED_HOSTS = ['https://shamelesis.com',
#                  'shamelesis.com',
#                  'ecom2-production-2c2f.up.railway.app',
#                  'https://ecom2-production-2c2f.up.railway.app']
# CSRF_TRUSTED_ORIGINS = ['https://shamelesis.com',
#                         'https://ecom2-production-2c2f.up.railway.app']
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'railway',
#         'USER': 'postgres',
#         'PASSWORD': os.environ['DB_PASSWORD'],
#          #// we use environmental password
#         'HOST': 'shuttle.proxy.rlwy.net',
#         'PORT': '18926',
#     }
# }
# # -------------------- END -----------------------


## ------------------------------------------------
## [Database 2] Local Database
## ------------------------------------------------
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
## -------------------- END -----------------------


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cart',
    'store',
    'payment',
    'whitenoise.runserver_nostatic',
    'paypal.standard.ipn',
    'cloudinary',
    'cloudinary_storage',
    'blog',
    'django_ckeditor_5',

    # google authentication
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # time system, to organize time
    'time_sys',

    # show "Thousands separator"
    'django.contrib.humanize',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    # google authentication
    "allauth.account.middleware.AccountMiddleware",
]


ROOT_URLCONF = 'ecom2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
                'store.context_processors.base_breadcrumbs',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecom2.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static/',
                    BASE_DIR / 'store' / 'static',]




# Cloudinary setup
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ['CLOUDINARY_CLOUD_NAME'],
    'API_KEY': os.environ['CLOUDINARY_API_KEY'],
    'API_SECRET': os.environ['CLOUDINARY_API_SECRET'],
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'



# CKEditor config
CKEDITOR_UPLOAD_PATH = "uploads/"  # will be a virtual path, not actual local
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_RESTRICT_BY_USER = True


# CKEditor 5 config
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|',
            'bold', 'italic', 'underline', 'strikethrough', '|',
            'link', 'blockQuote', 'code', 'codeBlock', '|',
            'bulletedList', 'numberedList', 'todoList', '|',
            'outdent', 'indent', '|',
            'mediaEmbed', 'insertTable', '|',
            'undo', 'redo', '|',
            'highlight', 'alignment', 'fontColor', 'fontBackgroundColor',
            'fontSize', 'fontFamily', '|',
            'horizontalLine', 'specialCharacters', 'pageBreak', 'findAndReplace',
        ],
        'image': {
            'toolbar': [
                'imageTextAlternative',
                'toggleImageCaption',
                'imageStyle:inline',
                'imageStyle:block',
                'imageStyle:side',
                'linkImage',
                'resizeImage'
            ]
        },
    }
}

CKEDITOR_UPLOAD_SLUGIFY_FILENAME = False
CKEDITOR_5_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
#CKEDITOR_5_FILE_STORAGE = "django.core.files.storage.DefaultStorage"


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
# MEDIA_URL = 'media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#// No MEDIA_ROOT needed due to Cloudinary

# whitenoise static stuff
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# add paypal settings
# set sandbox to true
PAYPAL_TEST = True
PAYPAL_RECEIVER_EMAIL = 'business@shamelesis.com'


#----------------------------------------------------
# Google Authentication
#----------------------------------------------------
SITE_ID = 1
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # default
    'allauth.account.auth_backends.AuthenticationBackend',  # allauth
)
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
#----------------------------------------------------
# remove email, username, password login
#----------------------------------------------------
ACCOUNT_LOGIN_METHODS = {"email"}  # replaces ACCOUNT_AUTHENTICATION_METHOD
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*"]  # replaces other 3
ACCOUNT_EMAIL_VERIFICATION = 'none'

# This removes email/password login options entirely from login form
SOCIALACCOUNT_ADAPTER = 'store.adapters.CustomSocialAccountAdapter'