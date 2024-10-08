from rest_framework import generics, permissions, status
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from datetime import datetime
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

class CreateUserView(generics.CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]  # hechqanday imkoniyatlarni cheklamaslik u-n


class VerifyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        code = self.request.data.get('code')

        self.check_verify(user, code)
        return Response(
            data={
                'success': True,
                'auth_status': user.auth_status,
                'access': user.token()['access'],
                'refresh': user.token()['refresh_token'],
            }
        )

    @staticmethod
    def check_verify(user, code):
        verify = user.verify_codes.filter(expiration_time__gte=datetime.now(), code=code, is_confirmed=False)
        if not verify.exists():
            data = {
                'message': 'Verification code is invalid',
            }
            raise ValidationError(data)
        else:
            verify.update(is_confirmed=True)

        if user.auth_status in [NEW, FORGET_PASS]:
            user.auth_status = CODE_VERIFIED
            user.save()
        return True


class GetNewVerifyCodeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        self.check_verification(user)
        if user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            send_email(user.email, code)

        elif user.auth_type == VIA_PHONE:
            code = user.create_verify_code(VIA_PHONE)
            send_email(user.phone_number, code)
            # send_phone_code(user.phone_number, code)
        else:
            data = {
                'message': 'Invalid verification code',
            }
            raise ValidationError(data)

        return Response(
            data={
                'success': True,
                'auth_status': user.auth_status,
                'access': user.token()['access'],
                'refresh': user.token()['refresh_token'],
            }
        )

    @staticmethod
    def check_verification(user):
        verify = user.verify_codes.filter(expiration_time__gte=datetime.now(), is_confirmed=False)
        if verify.exists():
            data = {
                'message': 'Kodingiz ishlatish uchun yaroqli',
            }
            raise ValidationError(data)


class ChangeUserView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangeUserSerializer
    http_method_names = ['put', 'patch', ]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        super(ChangeUserView, self).update(request, *args, **kwargs)
        data = {
            'success': True,
            'message': 'User updated',
            'auth_status': self.request.user.auth_status,
        }
        return Response(data)


class ChangePhotoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = ChangePhotoSerializer(data=request.data)
        if serializer.is_valid():
            user = self.request.user
            serializer.update(user, serializer.validated_data)
            return Response({
                "message": "User photo updated",
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class LoginRefreshView(TokenRefreshView):
    serializer_class = LoginRefreshSerializer


class LogoutView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = self.request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            data = {
                'success': True,
                'message': 'Logged out successfully'
            }
            return Response(data, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            data = {
                'message': 'Invalid refresh token'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        email_or_phone = serializer.validated_data.get(
            'email_or_phone')  # ['email_or_phone':'dbdbvdhbvdfhbv'] -- dbdbvdhbvdfhbv
        user = serializer.validated_data.get('user')

        if check_email_or_phone(email_or_phone) == 'phone':
            code = user.create_verify_code(VIA_PHONE)
            send_email(email_or_phone, code)
            # send_phone_code(email_or_phone, code)

        elif check_email_or_phone(email_or_phone) == 'email':
            code = user.create_verify_code(VIA_EMAIL)
            send_email(email_or_phone, code)

        user.auth_status = FORGET_PASS
        user.save()

        return Response(
            {
                "success": True,
                'message': "Tasdiqlash kodi muvaffaqiyatli yuborildi",
                "access": user.token()['access'],
                "refresh": user.token()['refresh_token'],
                "user_status": user.auth_status,
            }, status=status.HTTP_200_OK
        )


class ResetPasswordView(generics.UpdateAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    http_method_names = ['patch', 'put']

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        response = super(ResetPasswordView, self).update(request, *args, **kwargs)

        try:
            user = Users.objects.get(id=response.data.get('id'))

        except ObjectDoesNotExist as e:
            raise NotFound(detail='User topilmadi')

        return Response(
            {
                'success': True,
                'message': "Parolingiz muvaffaqiyatli o'zgartirildi",
                'access': user.token()['access'],
                'refresh': user.token()['refresh_token'],
                'auth_status': user.auth_status
            }
        )


class NewPhoneNumberView(APIView):
    serializer_class = UpdatePhoneNumberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        user = self.request.user
        serializer.is_valid(raise_exception=True)
        new_phone_number = serializer.validated_data.get('new_phone_number')

        if check_email_or_phone(new_phone_number) == 'phone':
            code = user.create_verify_code(VIA_PHONE)
            send_email(new_phone_number, code)

        user.new_phone = new_phone_number
        user.save()

        return Response(
            {
                'success': True,
                'message': "Cod muvaffaqiyatli yuborildi",
                'access': user.token()['access'],
                'refresh': user.token()['refresh_token'],
                'auth_status': user.auth_status
            }
        )


class VerifyAndUpdatePhoneNumberView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        code = self.request.data.get('code')

        self.check_verify(user, code)
        return Response(
            data={
                'success': True,
                'auth_status': user.auth_status,
                'access': user.token()['access'],
                'refresh': user.token()['refresh_token'],
            }
        )

    @staticmethod
    def check_verify(user, code):
        verify = user.verify_codes.filter(expiration_time__gte=datetime.now(), code=code, is_confirmed=False)
        if not verify.exists():
            data = {
                'message': 'Verification code is invalid',
            }
            raise ValidationError(data)
        else:
            verify.update(is_confirmed=True)

        if user.auth_status not in [NEW, FORGET_PASS, CODE_VERIFIED]:
            user.auth_status = DONE
            user.phone_number = user.new_phone
            user.new_phone = None
            user.save()
        return True
