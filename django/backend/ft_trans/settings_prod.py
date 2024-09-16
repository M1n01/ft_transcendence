"""
Django settings for ft_trans project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

LOG_BASE_DIR = os.path.join(BASE_DIR, "log")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s"
            + "{module}:{filename}:{funcName}:{lineno}"
            + "[%(levelname)s] %(message)s"
        }
    },
    "handlers": {
        "info": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_BASE_DIR, "info.log"),
            "formatter": "simple",
        },
        "warning": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_BASE_DIR, "warning.log"),
            "formatter": "simple",
        },
        "error": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_BASE_DIR, "error.log"),
            "formatter": "simple",
        },
    },
    "root": {
        "handlers": ["info", "warning", "error"],
        "level": "INFO",
    },
}


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    ".localhost",
    "127.0.0.1",
    "172.38.10.10",
    "nginx",
    "localhost",
    "localhost:8080",
    "localhost:443",
]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:8001",
    "http://localhost",
    "http://127.0.0.1",
    "http://172.38.10.10",
    "http://nginx",
    "https://nginx:443",
]


# Application definition

INSTALLED_APPS = [
    "daphne",  # ASGI設定
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "webpack_loader",
    "spa",
    "pong",
    "pong.score_keeper.apps.ScoreKeeperConfig",
    # "login",
    "accounts",
    # "accounts.models.ft_user",
    "web3",
]

MIDDLEWARE = [
    # "corsheaders.middleware.CorsMiddleware", #CORS設定
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # 多言語設定
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.LoginRequiredMiddleware",
    "django.contrib.auth.middleware.RemoteUserMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ft_trans.urls"

PROJECT_ROOT = os.path.join(BASE_DIR, "..")

# 出力ディレクトリ(nginxと共有)
PUBLIC_DIR = os.path.join(PROJECT_ROOT, "public")
# フロントエンド用ディレクトリ
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
# ブロックチェーン用ディレクトリ
BLOCKCHAIN_DIR = os.path.join(PROJECT_ROOT, "eth")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(FRONTEND_DIR, "src")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # alloauth
                # "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "ft_trans.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# """#PRODUCTION ENVIRONMENT
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "OPTIONS": {
            "service": "ft_trans",
            "passfile": ".my_pgpass",
            "sslmode": "prefer",
            "sslcert": "server.crt",
            "sslkey": "server.key",
        },
    }
}
# """  # PRODUCTION ENVIRONMENT

"""#DEVLOPMENT ENVIRONMENT
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
"""  # DEVLOPMENT ENVIRONMENT

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = [
    "accounts.oauth.FtOAuth",
    "accounts.backend.TmpUserBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# キャッシュ用
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# CSRF 不要
CSRF_USE_SESSIONS = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# ASGI設定
ASGI_APPLICATION = "ft_trans.asgi.application"

# 　多言語設定
LOCALE_PATHS = [
    os.path.join(BASE_DIR, "localization"),
]

STATIC_URL = "static/"
STATIC_ROOT = "./public/assets"
STATICFILES_DIRS = (os.path.join(PUBLIC_DIR, "static"),)

WEBPACK_LOADER = {
    "DEFAULT": {
        "BUNDLE_DIR_NAME": "webpack_bundles/",
        "STATS_FILE": os.path.join(PUBLIC_DIR, "webpack-stats.json"),
    }
}


LANGUAGE_CODE = "ja"
LANGUAGES = [
    ("ja", _("Japanese")),
    ("en", _("English")),
    ("fr", _("French")),
]

# CORS設定（暫定)
# CORS_ALLOWED_ORIGINS = [
# "https://localhost",
# "http://localhost:8000",
# ]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# HTTPS(TLS)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# X_FRAME_OPTIONS = 'DENY'


# 認証
LOGIN_REDIRECT_URL = "spa:index"  # Login後にリダイレクトされるページ
LOGOUT_REDIRECT_URL = "spa:index"  # Logout後にリダイレクトされるページ
AUTH_USER_MODEL = "accounts.FtUser"  # ユーザー認証用のモデル
SESSION_ENGINE = "django.contrib.sessions.backends.db"  # デフォルトのまま。セッションデータをDBに保存
LOGIN_URL = "accounts:login"

# OAUTH
OAUTH_AUTHORIZE_URL = "https://api.intra.42.fr/oauth/authorize"
OAUTH_CLIENT_ID = os.environ["OAUTH_CLIENT_ID"]
OAUTH_SECRET_ID = os.environ["OAUTH_SECRET_ID"]

# ドメイン
PONG_DOMAIN = "https://localhost/"

# エラーページ
ERROR_PAGE = PONG_DOMAIN + "error.html"

# WEB3
PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
PROVIDER_URL = "http://eth:8545"
PONG_SCORE_CONTRACT_ADDRESS = None

