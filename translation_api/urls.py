from django.urls import path
from .views import translate_category, run_migrate, translate_region_to_korean, get_place_info

urlpatterns = [
    path('translate/', translate_category, name='translate_category'),  # ✅ 경로 일치
    path('migrate/', run_migrate),
    path('translate/region/', translate_region_to_korean),
    path('place-info/', get_place_info, name='get_place_info')
]