import os

from shop_for_all.env import *

# Basic
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASIC_APP = "shop_for_all"
ROOT_URLCONF = f"{BASIC_APP}.urls"
WSGI_APPLICATION = f"{BASIC_APP}.wsgi.application"


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# CORS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = (
    "content-type",
    "accept-language",
    "accept",
    "origin",
    "authorization",
)


# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Rest Framework
REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_PAGINATION_CLASS": f"{BASIC_APP}.helpers.pagination.CustomPaginator",
    "PAGE_SIZE": 15,
}


# DRF-YASG Config
API_NAME = "Shop for All"
API_VERSION = "v0.1"
API_DESCRIPTION = "Shop for All API"

SWAGGER_SETTINGS = {
    "DEFAULT_AUTO_SCHEMA_CLASS": f"{BASIC_APP}.helpers.inspectors.swagger_auto_schema.SwaggerAutoSchema",
    "SECURITY_DEFINITIONS": {
        "Token": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
    "USE_SESSION_AUTH": False,
    "DEEP_LINKING": True,
    "DEFAULT_MODEL_RENDERING": "example",
    "DEFAULT_PAGINATOR_INSPECTORS": [
        f"{BASIC_APP}.helpers.inspectors.pagination.PaginatorInspector",
        "drf_yasg.inspectors.CoreAPICompatInspector",
    ],
}
