from django.urls import path
from .views import (translate_category, run_migrate, translate_region_to_korean, 
                    get_place_info, register, login_view, check_email_duplicate,
                    send_verification_code, verify_email_code,
                    send_password_reset_code, verify_reset_code, reset_password, update_username, delete_account)
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
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('email/send-code/', send_verification_code),
    path('email/verify-code/', verify_email_code),
    path('password/send-reset-code/', send_password_reset_code),
    path('password/verify_reset_code/', verify_reset_code),
    path('password/reset/', reset_password),
    path('user/update-name/', update_username),
    path('user/delete-account/', delete_account),
]