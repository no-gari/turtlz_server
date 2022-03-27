from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from api.user.serializers import UserRegisterSerializer, EmailVerifierCreateSerializer, \
    PhoneVerifierCreateSerializer, EmailVerifierConfirmSerializer, PhoneVerifierConfirmSerializer, \
    UserSocialLoginSerializer, UserDetailUpdateSerializer


class UserSocialLoginView(CreateAPIView):
    serializer_class = UserSocialLoginSerializer


class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer


class UserDetailUpdateView(RetrieveUpdateAPIView):
    serializer_class = UserDetailUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class EmailVerifierCreateView(CreateAPIView):
    serializer_class = EmailVerifierCreateSerializer


class EmailVerifierConfirmView(CreateAPIView):
    serializer_class = EmailVerifierConfirmSerializer


class PhoneVerifierCreateView(CreateAPIView):
    serializer_class = PhoneVerifierCreateSerializer


class PhoneVerifierConfirmView(CreateAPIView):
    serializer_class = PhoneVerifierConfirmSerializer
