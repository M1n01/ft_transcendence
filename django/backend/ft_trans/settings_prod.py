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
    "notification",
    "pong",
    "tournament",
    "friend",
    "history",
    # "login",
    "accounts",
    # "accounts.models.ft_user",
    # "api",
    "sendgrid",
    "django_celery_results",
    "users",
    "channels",
    "ws",
    "web3",
]

MIDDLEWARE = [
    # "corsheaders.middleware.CorsMiddleware", #CORS設定
    "django.middleware.security.SecurityMiddleware",
    # "django.contrib.sessions.middleware.SessionMiddleware",
    "accounts.middleware.CustomSessionMiddleware",  # SessionMiddlewareの改造品
    "django.middleware.locale.LocaleMiddleware",  # 多言語設定
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.LoginRequiredMiddleware",
    "django.contrib.auth.middleware.RemoteUserMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "users.middleware.UserActionLoggingMiddleware",  # Log保管用
]

ROOT_URLCONF = "ft_trans.urls"

PROJECT_ROOT = os.path.join(BASE_DIR, "..")

# 出力ディレクトリ(nginxと共有)
PUBLIC_DIR = os.path.join(PROJECT_ROOT, "public")
# フロントエンド用ディレクトリ
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
# ブロックチェーン用ディレクトリ
BLOCKCHAIN_DIR = os.path.join(PROJECT_ROOT, "eth")

# メディア
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(PUBLIC_DIR, "media/")

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

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}
# CHANNEL_LAYERS = {
#    "default": {
#        "BACKEND": "channels_redis.core.RedisChannelLayer",
#        "CONFIG": {
#            "hosts": [
#                f"rediss://default:{os.environ['REDIS_PASSOWRD']}@172.38.30.30:6379"
#            ],
#        },
#    },
# }

WS = "wss"

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
    "accounts.backend.FtUserBackend",
    "accounts.backend.TmpUserBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# キャッシュ用
# CACHES = {
#    "default": {
#        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
#        "LOCATION": "unique-snowflake",
#    }
# }
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"rediss://default:{os.environ['REDIS_PASSOWRD']}@172.38.30.30:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SSL_CERT_REQS": None,  # SSL証明書の検証をスキップ
        },
    }
}
REDIS_SERVER = "redis"
REDIS_PORT = 6379
REDIS_SSL = True
REDIS_PASSWORD = os.environ["REDIS_PASSOWRD"]

# Celery configurations
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZZER = "json"
# CELERY_TIMEZONE = TIME_ZONE


# 'amqp://guest:guest@localhost//'
# celeryを動かすための設定ファイル
# CELERY_BROKER_URL = "http://localhost:6379/0"
# CELERY_BROKER_URL = "redis://redis:6379"
# CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_CACHE_BACKEND = "django-cache"

# Celery設定
# CELERY_BROKER_URL = os.environ.get("REDIS_URL", "redis://redis:6379/1")
CELERY_BROKER_URL = (
    f"rediss://default:{os.environ['REDIS_PASSOWRD']}@172.38.30.30:6379/1"
)
CELERY_RESULT_BACKEND = "django-db"
# CELERY_RESULT_BACKEND = (
# f"rediss://default:{os.environ['REDIS_PASSOWRD']}@172.38.10.30:6379"
# )

CELERY_RESULT_EXTENDED = True

CELERYD_CONCURRENCY = 1

CELERYD_LOG_FILE = "../log/celeryd.log"

# CELERYD_LOG_LEVELをINFOにしておくと、
# タスクの標準出力もログ(celeryd.log)に書かれる
CELERYD_LOG_LEVEL = "INFO"


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

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# HTTPS(TLS)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# 認証
LOGIN_REDIRECT_URL = "spa:top"  # Login後にリダイレクトされるページ
LOGOUT_REDIRECT_URL = "spa:top"  # Logout後にリダイレクトされるページ
AUTH_USER_MODEL = "accounts.FtUser"  # ユーザー認証用のモデル
SESSION_ENGINE = "django.contrib.sessions.backends.db"  # デフォルトのまま。セッションデータをDBに保存
LOGIN_URL = "spa:to-login"

# OAUTH
OAUTH_AUTHORIZE_URL = "https://api.intra.42.fr/oauth/authorize"
OAUTH_CLIENT_ID = os.environ["OAUTH_CLIENT_ID"]
OAUTH_SECRET_ID = os.environ["OAUTH_SECRET_ID"]

# 2FA
TWO_FA_AUTH_KEY = os.environ["TWO_FA_AUTH_KEY"]

# ドメイン
PONG_DOMAIN = "https://localhost/"

# エラーページ
ERROR_PAGE = PONG_DOMAIN + "error.html"

# SEND_GRID
SENDGRID_EMAIL_HOST = "smtp.sendgrid.net"
SENDGRID_EMAIL_PORT = 587
SENDGRID_EMAIL_USERNAME = "your_sendgrid_username"
SENDGRID_EMAIL_PASSWORD = "your_sendgrid_password"

# TWILIO(SMS)
TWILIO_SERVICE_SID = os.environ["TWILIO_SERVICE_SID"]
TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]

# Brevo(Email)
BREVO_API_KEY = os.environ["BREVO_API_KEY"]
BREVO_SENDER_ADDRESS = os.environ["BREVO_SENDER_ADDRESS"]

# JWT有効期限
JWT_TMP_VALID_TIME = 300
JWT_VALID_TIME = 14400

# timezon #時間にはJTC固定とする
# ただし、内部的にはUTCで保存する
TIME_HOURS = 9

# WEB3
PRIVATE_ACCOUNT_KEY = os.environ["PRIVATE_ACCOUNT_KEY"]
PROVIDER_URL = os.environ["PROVIDER_URL"]
CONTRACT_ADDRESS = os.environ["CONTRACT_ADDRESS"]

# const
USERNAME_MAX_LEN = 16
LASTNAME_MAX_LEN = 64
FIRSTNAME_MAX_LEN = 64
EMAIL_MAX_LEN = 90
PHONE_MAX_LEN = 15
PASSWORD_MIN_LEN = 8
PASSWORD_MAX_LEN = 20
TOURNAMENTNAME_MAX_LEN = 20
