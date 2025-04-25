from django.urls import path
from .views import translate_category, run_migrate, translate_region_to_korean, get_place_info, register, login_view, check_email_duplicate
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('translate/', translate_category, name='translate_category'),  # ✅ 경로 일치
    path('migrate/', run_migrate),
    path('translate/region/', translate_region_to_korean),
    path('place-info/', get_place_info, name='get_place_info'),
    path('register/', register),
    path('login/', login_view),
    path('check-email/', check_email_duplicate),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]