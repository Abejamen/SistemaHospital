from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "dev-key"
DEBUG = True
ALLOWED_HOSTS = []

# APPS
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "usuarios",
    "core",
    "formularios",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.mfa",
    "axes",
    "preventconcurrentlogins",
    "django_extensions",
]

SITE_ID = 1

# AUTENTICACIÓN
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "axes.backends.AxesStandaloneBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",

    # Necesario para Allauth
    "allauth.account.middleware.AccountMiddleware",

    # Seguridad
    "axes.middleware.AxesMiddleware",
    "preventconcurrentlogins.middleware.PreventConcurrentLoginsMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# URLs
ROOT_URLCONF = "sistema_hospital.urls"

# TEMPLATES
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # carpeta templates principal
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

WSGI_APPLICATION = "sistema_hospital.wsgi.application"

# BASE DE DATOS (MySQL)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "sistema_hospital",
        "USER": "root",
        "PASSWORD": "12345678",
        "HOST": "localhost",
        "PORT": "3306",
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}

# INTERNACIONALIZACIÓN
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

# ARCHIVOS ESTÁTICOS
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



# Método de login
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"

# Verificación de email: NONE para que no bloquee nada en desarrollo
ACCOUNT_EMAIL_VERIFICATION = "none"

# Permitir registro de usuarios (ANTES ESTABA BLOQUEADO)
ACCOUNT_ALLOW_REGISTRATION = True
ACCOUNT_SIGNUP_ALLOWED = True

# Custom forms
ACCOUNT_FORMS = {
    "login": "usuarios.forms.CustomLoginForm",
    "signup": "usuarios.forms.CustomSignupForm",
}

# Plantilla personalizada para REGISTRO
ACCOUNT_SIGNUP_TEMPLATE = "account/registro.html"

# Redirecciones
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/"

# Allauth logout inmediato
ACCOUNT_LOGOUT_ON_GET = True

AUTH_USER_MODEL = "usuarios.Usuario"