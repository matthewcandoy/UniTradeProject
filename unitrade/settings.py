from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-y_2v*(wlez6hm^mtpd6qkb$r32wql*u_es^-70nm0iz^#&jljx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['unitradeproject.onrender.com', 'localhost', '127.0.0.1']

# Session and login settings
CART_SESSION_ID = 'cart'
SESSION_COOKIE_AGE = 86400
LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'myaccount'
LOGOUT_REDIRECT_URL = 'frontpage'
ACCOUNT_LOGOUT_REDIRECT_URL = 'login'

# Google OAuth settings for django-allauth

SOCIALACCOUNT_AUTO_SIGNUP = True

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '863824603941-bbhravgud368moq1e2hnvavgb85cd5dq.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'REDIRECT_URI': 'https://unitradeproject.onrender.com/accounts/google/login/callback/',
    }
}


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'core',
    'store',
    'userprofile',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'unitrade.urls'

WEBSITE_URL = 'https://unitradeproject.onrender.com/'

STRIPE_PUB_KEY = 'pk_test_51ROhnDFCwS1HirRLdip6IBPkiUPHxv3u6sUIzIdMCrMsq7QaqpQkwSORxn5i5YND0BEIkml2ViWa1N0z0FBUcw9400HNKwIVym'
STRIPE_SECRET_KEY = 'sk_test_51ROhnDFCwS1HirRLHFdfiv0CTOqcmOMAmlUlDeCk3OxBpREaxeHyaofC5TNkXWOyyy7BivCEl2REtLQBckFnopfa004UsxHhwt'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'unitrade.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Site ID for django.contrib.sites
SITE_ID = 1

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
