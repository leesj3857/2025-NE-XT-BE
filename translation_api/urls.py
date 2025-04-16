from django.urls import path
from .views import translate_category, run_migrate

urlpatterns = [
    path('translate/', translate_category, name='translate_category'),  # ✅ 경로 일치
    path('migrate/', run_migrate),
]