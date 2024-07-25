from django.urls import path
from .views import sign_up, log_in, log_out, otp_verification , resend_otp, forgot_password, change_password
from . profile import user_profile, order_detail, make_default_address

urlpatterns = [
    path('', log_in, name="logIn"),
    path('signup/', sign_up, name="signup"),
    path('otpVerify/<str:key>/', otp_verification, name="otp_verification"),
    path('resend_otp/<str:key>/', resend_otp, name="resend_otp"),
    path('logout/', log_out, name="logout"),
    path('forgot-password/', forgot_password, name="forgotpassword"),
    path('change-password/<str:encrypt_id>/', change_password, name="changepassword"),
    path('user-profile/', user_profile, name="user_profile"),
    path('user-profile/order/<int:id>', order_detail, name="order_detail"),
    path('make-default-address/', make_default_address, name="make-default-address"),
]