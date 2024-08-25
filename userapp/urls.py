from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', CreateUserView.as_view()),
    path('verify/', VerifyAPIView.as_view()),
    path('new_verify/', GetNewVerifyCodeView.as_view()),
    path('registration/', ChangeUserView.as_view()),
    path('change_photo/', ChangePhotoView.as_view()),
]
