import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
INSTALLED_APPS = [
    'django.contrib.admin',          # ✅ admin 페이지 관련
    'django.contrib.auth',           # ✅ 사용자 인증
    'django.contrib.contenttypes',   # ✅ 모델 간 관계
    'django.contrib.sessions',       # ✅ 세션 관리
    'django.contrib.messages',       # ✅ 메시징
    'django.contrib.staticfiles',    # ✅ 정적 파일 제공
    'corsheaders',

    # 여기에 직접 만든 앱도 추가
    'translation_api',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    }
}
AUTH_USER_MODEL = 'translation_api.User'
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

DEBUG = True

ALLOWED_HOSTS = ['*']

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # ✅ 필수
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # ✅ 필수
    'django.contrib.messages.middleware.MessageMiddleware',  # ✅ 필수
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
STATIC_URL = '/static/'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://koreat.netlify.app",
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# Optional: 토큰 유효기간 등 설정
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}