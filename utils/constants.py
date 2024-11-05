from dotenv import dotenv_values

env = dotenv_values(".env")


# Settings Constants
# =====================================================
class Settings:
    """Settings Constants"""

    SECRET_KEY = env.get("SECRET_KEY")
    ROOT_URLCONF = "quickpnr.urls"
    AUTH_USER_MODEL = "users.User"
    WSGI_APPLICATION = "quickpnr.wsgi.application"
    DATABASE_URL = env.get("DATABASE_URL")
    LANGUAGE_CODE = "en-us"
    TIME_ZONE = "Asia/Kolkata"
    USE_I18N = True
    USE_TZ = True
    STATIC_URL = "static/"
    STATIC_ROOT = "assets/"
    STATIC_FILES_DIRS = "templates/static/"
    TEMPLATES_URLS = "templates/"
    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
    REDIS_URL = env.get("REDIS_URL")
    MEDIA_URL = "media/"
    MEDIA_ROOT = "media/"


# Email Configurations
# =====================================================
class EmailConfig:
    """Email Configurations"""

    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    PORT_465 = 465
    PORT_587 = 587
    EMAIL_HOST_USER = env.get("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env.get("EMAIL_HOST_PASSWORD")


# Celery Configuration
# =====================================================
class CeleryConfig:
    """Celery Configuration"""

    CELERY_BROKER_URL = "redis://localhost:6379/0"
