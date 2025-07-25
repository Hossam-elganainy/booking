from django.urls import path
from .views import (
    ChangePasswordView,
    RequestOTPView,
    VerifyOTPView,
    ResetPasswordWithOTPView,
    LoginView,
    RegisterView,
    UserProfileView,
)

urlpatterns = [
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("request-otp/", RequestOTPView.as_view(), name="request_otp"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify_otp"),
    path("reset-password-with-otp/", ResetPasswordWithOTPView.as_view(), name="reset_password_with_otp"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", UserProfileView.as_view(), name="profile"),
]
