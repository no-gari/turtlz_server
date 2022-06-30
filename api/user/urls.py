from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.user.views import UserRegisterView, PhoneVerifierCreateView, PhoneVerifierConfirmView, \
    UserSocialLoginView, UserDetailUpdateView, ProfileDetailUpdateView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('social_login/', UserSocialLoginView.as_view()),
    path('email_login/', UserRegisterView.as_view()),
    path('email_signup/', UserRegisterView.as_view()),
    path('profile/', ProfileDetailUpdateView.as_view()),
    path('update/', UserDetailUpdateView.as_view()),
    path('phone_verifier/', PhoneVerifierCreateView.as_view()),
    path('phone_verifier/confirm/', PhoneVerifierConfirmView.as_view()),
]
