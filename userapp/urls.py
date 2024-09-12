from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', CreateUserView.as_view()),
    path('verify/', VerifyAPIView.as_view()),
    path('new_verify/', GetNewVerifyCodeView.as_view()),
    path('registration/', ChangeUserView.as_view()),
    path('change_photo/', ChangePhotoView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('login_refresh/', LoginRefreshView.as_view()),
    path('forgot_password/', ForgotPasswordView.as_view()),
    path('reset_password/', ResetPasswordView.as_view()),
    path('new_phone/', NewPhoneNumberView.as_view()),
    path('update_new_phone/', VerifyAndUpdatePhoneNumberView.as_view())
]
