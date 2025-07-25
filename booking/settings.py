from datetime import timedelta
import os,sys
from pathlib import Path
import environ
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add this line to include the apps folder in the PYTHONPATH
env = environ.Env()
env.read_env(env.str(str(BASE_DIR), ".env"))


SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG", cast=bool)
ALLOWED_HOSTS = env("ALLOWED_HOSTS", cast=list)
CORS_ALLOW_ALL_ORIGINS = True
# SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    # 'ckeditor',
    "corsheaders",
    "drf_yasg",
    "book",
    "users",
    'reservations',
]


UNFOLD = {
    "SHOW_LANGUAGES": True,
    "SITE_TITLE": "Madinah",
    "SITE_HEADER": "Madinah",
    "SITE_SUBHEADER": "Madinah",
    # "SITE_DROPDOWN": [
    #     {
    #         "icon": "diamond",
    #         "title": _("My site"),
    #         "link": "https://example.com",
    #     },
    #     # ...
    # ],
    # "SITE_URL": "/",
    # # "SITE_ICON": lambda request: static("icon.svg"),  # both modes, optimise for 32px height
    # "SITE_ICON": {
    #     "light": lambda request: static("icon-light.svg"),  # light mode
    #     "dark": lambda request: static("icon-dark.svg"),  # dark mode
    # },
    # # "SITE_LOGO": lambda request: static("logo.svg"),  # both modes, optimise for 32px height
    # "SITE_LOGO": {
    #     "light": lambda request: static("logo-light.svg"),  # light mode
    #     "dark": lambda request: static("logo-dark.svg"),  # dark mode
    # },
    # "SITE_SYMBOL": "speed",  # symbol from icon set
    # "SITE_FAVICONS": [
    #     {
    #         "rel": "icon",
    #         "sizes": "32x32",
    #         "type": "image/svg+xml",
    #         "href": lambda request: static("favicon.svg"),
    #     },
    # ],
    # "SHOW_HISTORY": True, # show/hide "History" button, default: True
    # "SHOW_VIEW_ON_SITE": True, # show/hide "View on site" button, default: True
    # "SHOW_BACK_BUTTON": False, # show/hide "Back" button on changeform in header, default: False
    # "ENVIRONMENT": "sample_app.environment_callback", # environment name in header
    # "ENVIRONMENT_TITLE_PREFIX": "sample_app.environment_title_prefix_callback", # environment name prefix in title tag
    # "DASHBOARD_CALLBACK": "sample_app.dashboard_callback",
    # "THEME": "dark", # Force theme: "dark" or "light". Will disable theme switcher
    # "LOGIN": {
    #     "image": lambda request: static("sample/login-bg.jpg"),
    #     "redirect_after": lambda request: reverse_lazy("admin:APP_MODEL_changelist"),
    # },
    # "STYLES": [
    #     lambda request: static("css/style.css"),
    # ],
    # "SCRIPTS": [
    #     lambda request: static("js/script.js"),
    # ],
    # "BORDER_RADIUS": "6px",
    "COLORS": {
        "base": {
            "50": "249 250 251",
            "100": "243 244 246",
            "200": "229 231 235",
            "300": "209 213 219",
            "400": "156 163 175",
            "500": "107 114 128",
            "600": "75 85 99",
            "700": "55 65 81",
            "800": "31 41 55",
            "900": "17 24 39",
            "950": "3 7 18",
        },
        "primary": {
            "50": "240 253 250",  # Very light teal, almost white
            "100": "204 251 241",  # Light teal
            "200": "153 246 228",  # Lighter teal
            "300": "94 234 212",   # Soft teal
            "400": "45 212 191",   # Medium teal
            "500": "20 184 166",   # Base teal (strong & vibrant)
            "600": "13 148 136",   # Darker teal
            "700": "15 118 110",   # Even darker teal
            "800": "17 94 89",     # Deep teal
            "900": "19 78 74",     # Very deep teal
            "950": "4 47 46"       # Almost black-teal
        },
        "font": {
            "subtle-light": "var(--color-base-500)",  # text-base-500
            "subtle-dark": "var(--color-base-400)",  # text-base-400
            "default-light": "var(--color-base-600)",  # text-base-600
            "default-dark": "var(--color-base-300)",  # text-base-300
            "important-light": "var(--color-base-900)",  # text-base-900
            "important-dark": "var(--color-base-100)",  # text-base-100
        },
    },
    # "EXTENSIONS": {
    #     "modeltranslation": {
    #         "flags": {
    #             "en": "🇬🇧",
    #             "fr": "🇫🇷",
    #             "nl": "🇧🇪",
    #         },
    #     },
    # },
    "SIDEBAR": {
        "show_search": False,  # Search in applications and models names
        "show_all_applications": False,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _("Navigation"),
                "separator": True,  # Top border
                "collapsible": True,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                        # "badge": "sample_app.badge_callback",
                        "permission": lambda request: request.user.has_perm("users.view_dashboard"),
                    },
                    # {
                    #     "title": _("Projects"),
                    #     "icon": "projects",  # Supported icon set: https://fonts.google.com/icons
                    #     "link": reverse_lazy("admin:projects_project_changelist"),
                    # },
 
                    # groups permissions
                    # {
                    #     "title": _("Permissions"),
                    #     "icon": "group",
                    #     "link": reverse_lazy("admin:auth_permission_changelist"),
                    #     "permission": lambda request: request.user.is_superuser,
                    # },
                ],
            },
        ],
    },
    # "TABS": [
    #     {
    #         "models": [
    #             "branches.branch",
    #         ],
    #         "items": [
    #             {
    #                 "title": _("branches"),
    #                 "link": reverse_lazy("admin:branches_branch_changelist"),
    #                 # "permission": "sample_app.permission_callback",
    #             },
    #         ],
    #     },
    # ],
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'corsheaders.middleware.CorsMiddleware',
]
REST_FRAMEWORK = { 
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}


ROOT_URLCONF = "booking.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "booking.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        },
    },
    'USE_SESSION_AUTH': False,
    'api_version': '1.0',
    'enabled_methods': ['get', 'post', 'put', 'patch', 'delete'],
}
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {"default": env.db()}



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Define supported languages (e.g., English and Arabic)
LANGUAGES = [
    ('en', 'English'),
    ('ar', 'Arabic'),
]

# Default language (can be overridden by user selection)
LANGUAGE_CODE = 'en'

# Directory for translation files
LOCALE_PATHS = [
    BASE_DIR + '/locale',  # e.g., /path/to/your/project/locale/
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = env("STATIC_URL")
STATIC_ROOT = env("STATIC_ROOT")

MEDIA_URL = env("MEDIA_URL")
MEDIA_ROOT = env("MEDIA_ROOT")
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"