import jwt
import random
import hashlib
import requests
from django.conf import settings
from urllib.parse import urlparse
from django.db import transaction
from django.utils import timezone
from api.logger.models import PhoneLog
from rest_framework import serializers
from django.core.files.base import ContentFile
from api.user.validators import validate_password
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError as DjangoValidationError
from api.user.models import User, EmailVerifier, PhoneVerifier, Social, SocialKindChoices, Profile


class UserSocialLoginSerializer(serializers.Serializer):
    code = serializers.CharField(write_only=True)
    state = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        code = attrs['code']
        state = attrs['state']

        if state in SocialKindChoices:
            attrs['social_user_attributes'] = self.get_social_user_id(code, state)
        else:
            raise ValidationError({'kind': '지원하지 않는 소셜 타입입니다.'})

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        state = validated_data['state']
        email = validated_data['social_user_attributes']['email']
        nickname = validated_data['social_user_attributes']['nickname']
        profile_image_url = validated_data['social_user_attributes']['profile_image_url']
        user, created = User.objects.get_or_create(email=email, defaults={'password': make_password(None)})

        if created:
            user_profile = Profile.objects.create(user=user, nickname=nickname, kind=state)
            if profile_image_url != '':
                name = urlparse(profile_image_url).path.split('/')[-1]
                response = requests.get(profile_image_url)
                user_profile.image.save(name, ContentFile(response.content), save=True)
            user_profile.save()

        refresh = RefreshToken.for_user(user)
        return {
            'access': refresh.access_token,
            'refresh': refresh,
        }

    def get_social_user_id(self, code, state):
        social_user_id = getattr(self, f'get_{state}_user_id')(code)
        return social_user_id

    def get_kakao_user_id(self, code):
        url = 'https://kauth.kakao.com/oauth/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': settings.KAKAO_CLIENT_ID,
            'redirect_uri': settings.SOCIAL_REDIRECT_URL,
            'code': code,
            'client_secret': settings.KAKAO_CLIENT_SECRET,
        }
        response = requests.post(url=url, data=data)
        if not response.ok:
            raise ValidationError('KAKAO GET TOKEN API ERROR')
        data = response.json()

        url = 'https://kapi.kakao.com/v2/user/me'
        headers = {
            'Authorization': f'Bearer {data["access_token"]}'
        }
        response = requests.get(url=url, headers=headers)
        if not response.ok:
            raise ValidationError('KAKAO ME API ERROR')
        data = response.json()
        email = data['kakao_account'].get("email") if data['kakao_account'].get('has_email') is True else data['id'] + '@email.com'
        nickname = data['properties'].get('nickname', '')
        profile_image_url = data['properties'].get('profile_image', '')
        return {'email': email, 'nickname': nickname, 'profile_image_url': profile_image_url}

    def get_apple_user_id(self, code):
        url = 'https://appleid.apple.com/auth/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': settings.APPLE_CLIENT_ID,
            'client_secret': settings.APPLE_CLIENT_SECRET,
            'redirect_uri': settings.SOCIAL_REDIRECT_URL,
            'code': code,
        }
        response = requests.post(url=url, data=data)
        if not response.ok:
            raise ValidationError('APPLE GET TOKEN API ERROR')
        data = response.json()
        decoded_user = jwt.decode(data['user'], '', verify=False)
        email = decoded_user['email']
        nickname = decoded_user['name'].get('firstName', '')
        profile_image_url = ''
        return {'email': email, 'nickname': nickname, 'profile_image_url': profile_image_url}


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True, required=False)
    email_token = serializers.CharField(write_only=True, required=False)
    name = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True, required=False)
    phone_token = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    password_confirm = serializers.CharField(write_only=True, required=False)

    access = serializers.CharField()
    refresh = serializers.CharField(read_only=True)

    def get_fields(self):
        fields = super().get_fields()

        if 'email' in User.VERIFY_FIELDS:
            fields['email_token'].required = True
        if 'email' in User.VERIFY_FIELDS or 'email' in User.REGISTER_FIELDS:
            fields['email'].required = True
        if 'phone' in User.VERIFY_FIELDS:
            fields['phone_token'].required = True
        if 'phone' in User.VERIFY_FIELDS or 'phone' in User.REGISTER_FIELDS:
            fields['phone'].required = True
        if 'password' in User.REGISTER_FIELDS:
            fields['password'].required = True
            fields['password_confirm'].required = True

        return fields

    def validate(self, attrs):
        email = attrs.get('email')
        email_token = attrs.pop('email_token', None)
        phone = attrs.get('phone')
        phone_token = attrs.pop('phone_token', None)

        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm', None)

        if 'email' in User.VERIFY_FIELDS:
            # 이메일 토큰 검증
            try:
                self.email_verifier = EmailVerifier.objects.get(email=email, token=email_token)
            except EmailVerifier.DoesNotExist:
                raise ValidationError('이메일 인증을 진행해주세요.')
        if 'email' in User.VERIFY_FIELDS or 'email' in User.REGISTER_FIELDS:
            # 이메일 검증
            if User.objects.filter(email=email).exists():
                raise ValidationError({'email': ['이미 가입된 이메일입니다.']})

        if 'phone' in User.VERIFY_FIELDS:
            # 휴대폰 토큰 검증
            try:
                self.phone_verifier = PhoneVerifier.objects.get(phone=phone, token=phone_token)
            except PhoneVerifier.DoesNotExist:
                raise ValidationError('휴대폰 인증을 진행해주세요.')
        if 'phone' in User.VERIFY_FIELDS or 'phone' in User.REGISTER_FIELDS:
            # 휴대폰 검증
            if User.objects.filter(phone=phone).exists():
                raise ValidationError({'phone': ['이미 가입된 휴대폰입니다.']})

        if 'password' in User.REGISTER_FIELDS:
            errors = {}
            # 비밀번호 검증
            if password != password_confirm:
                errors['password'] = ['비밀번호가 일치하지 않습니다.']
                errors['password_confirm'] = ['비밀번호가 일치하지 않습니다.']
            else:
                try:
                    validate_password(password)
                except DjangoValidationError as error:
                    errors['password'] = list(error)
                    errors['password_confirm'] = list(error)

            if errors:
                raise ValidationError(errors)

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data,
        )
        Profile.objects.create(user=user)
        if 'email' in User.VERIFY_FIELDS:
            self.email_verifier.delete()
        if 'phone' in User.VERIFY_FIELDS:
            self.phone_verifier.delete()

        refresh = RefreshToken.for_user(user)

        return {
            'access': refresh.access_token,
            'refresh': refresh,
        }


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['user']


class UserDetailUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True, allow_blank=True)
    password_confirm = serializers.CharField(write_only=True, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password', 'password_confirm']

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        errors = {}

        # 이메일 검증
        if self.instance.is_social:
            attrs['email'] = self.instance.email

        # 비밀번호 검증
        if password or password_confirm:
            if password != password_confirm:
                errors['password'] = ['비밀번호가 일치하지 않습니다.']
                errors['password_confirm'] = ['비밀번호가 일치하지 않습니다.']
            else:
                try:
                    validate_password(password)
                except DjangoValidationError as error:
                    errors['password'] = list(error)
                    errors['password_confirm'] = list(error)
            attrs['password'] = make_password(password)
        else:
            attrs['password'] = self.instance.password

        if errors:
            raise ValidationError(errors)

        return attrs

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.__dict__.update(validated_data)
        instance.save()
        return instance


class EmailVerifierCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerifier
        fields = ['email']

    def validate(self, attrs):
        email = attrs['email']

        if User.objects.filter(email=email).exists():
            raise ValidationError({'email': ['이미 존재하는 이메일입니다.']})

        code = ''.join([str(random.randint(0, 9)) for i in range(6)])
        created = timezone.now()
        hash_string = str(email) + code + str(created.timestamp())
        token = hashlib.sha1(hash_string.encode('utf-8')).hexdigest()

        attrs.update({
            'code': code,
            'token': token,
            'created': created,
        })

        try:
            self.send_code(attrs)
        except Exception:
            raise ValidationError('인증번호 전송 실패')

        return attrs

    def send_code(self, attrs):
        body = f'아키디카 회원가입 인증번호: [{attrs["code"]}]'
        PhoneLog.objects.create(to=attrs['phone'], body=body)


class EmailVerifierConfirmSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    code = serializers.CharField(write_only=True)
    email_token = serializers.CharField(read_only=True, source='token')

    class Meta:
        model = EmailVerifier
        fields = ['email', 'code', 'email_token']

    def validate(self, attrs):
        email = attrs['email']
        code = attrs['code']
        try:
            email_verifier = self.Meta.model.objects.get(email=email, code=code)
        except self.Meta.model.DoesNotExist:
            raise ValidationError({'code': ['인증번호가 일치하지 않습니다.']})

        attrs.update({'token': email_verifier.token})
        return attrs

    def create(self, validated_data):
        return validated_data


class PhoneVerifierCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneVerifier
        fields = ['phone']

    def validate(self, attrs):
        phone = attrs['phone']

        if User.objects.filter(phone=phone).exists():
            raise ValidationError({'phone': ['이미 존재하는 휴대폰입니다.']})

        code = ''.join([str(random.randint(0, 9)) for i in range(6)])
        created = timezone.now()
        hash_string = str(phone) + code + str(created.timestamp())
        token = hashlib.sha1(hash_string.encode('utf-8')).hexdigest()

        attrs.update({
            'code': code,
            'token': token,
            'created': created,
        })

        try:
            self.send_code(attrs)
        except Exception:
            raise ValidationError('인증번호 전송 실패')

        return attrs

    def send_code(self, attrs):
        pass


class PhoneVerifierConfirmSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True)
    code = serializers.CharField(write_only=True)
    phone_token = serializers.CharField(read_only=True, source='token')

    class Meta:
        model = PhoneVerifier
        fields = ['phone', 'code', 'phone_token']

    def validate(self, attrs):
        phone = attrs['phone']
        code = attrs['code']
        try:
            phone_verifier = self.Meta.model.objects.get(phone=phone, code=code)
        except self.Meta.model.DoesNotExist:
            raise ValidationError({'code': ['인증번호가 일치하지 않습니다.']})

        attrs.update({'token': phone_verifier.token})
        return attrs

    def create(self, validated_data):
        return validated_data
