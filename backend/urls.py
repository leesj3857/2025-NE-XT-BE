# backend/urls.py
from django.contrib import admin
from django.urls import path, include
# ✅ 잘못된 import 제거: translate_text 대신 translate_category 또는 그냥 제거

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('translation_api.urls')),  # /api/translate/ 경로로 연결됨
]
