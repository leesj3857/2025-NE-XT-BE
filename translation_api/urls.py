from django.urls import path
from .views import translate_category

urlpatterns = [
    path('translate/', translate_category, name='translate_category'),  # ✅ 경로 일치
]