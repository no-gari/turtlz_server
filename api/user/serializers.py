import random
import hashlib
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from api.logger.models import PhoneLog
from rest_framework import serializers
from django.core.validators import validate_email
from api.user.validators import validate_password
from api.clayful_client import ClayfulCustomerClient
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError as DjangoValidationError
from api.user.models import User, EmailVerifier, PhoneVerifier, SocialKindChoices, Profile


class UserSocialLoginSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    code = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)
    nickname = serializers.CharField(write_only=True)
    social_type = serializers.CharField(write_only=True)

    def validate(self, attrs):
        code = attrs['code']
        email = attrs['email']
        nickname = attrs['nickname']
        social_type = attrs['social_type']

        if social_type not in SocialKindChoices:
            raise ValidationError({'kind': '지원하지 않는 소셜 타입입니다.'})

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        code = validated_data['code']
        email = validated_data['email']
        nickname = validated_data['nickname']
        social_type = validated_data['social_type']
        user, created = User.objects.get_or_create(email=email, defaults={'password': make_password(None)})

        if created:
            clayful_customer_client = ClayfulCustomerClient()
            clayful_register = clayful_customer_client.clayful_register(email=email, nickname=nickname)

            if not clayful_register.status == 201:
                user.delete()
                raise ValidationError({'error_msg': '서버 에러입니다. 다시 시도해주세요.'})
            else:
                clayful_login = clayful_customer_client.clayful_login(email=email)
                token = clayful_login.data['token']
                user_id = clayful_login.data['customer']

            user_profile = Profile.objects.create(user=user, clayful_token=token, nickname=nickname, kind=social_type, code=code)
            clayful_customer_client.clayful_customer_add_coupon(customer_id=user_id, coupon_id=settings.CLAYFUL_COUPON_ID)
            user_profile.save()

        refresh = RefreshToken.for_user(user)
        return {
            'access': refresh.access_token,
            'refresh': refresh,
        }


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get('email')

        if 'email' in User.REGISTER_FIELDS:
            if User.objects.filter(email=email).exists():
                raise ValidationError({'email': ['이미 가입된 이메일입니다.']})
        return attrs

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']

        try:
            validate_email(email)
        except:
            raise ValidationError({'error_msg': '이메일 형식이 아닙니다.'})

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        user, created = User.objects.get_or_create(email=email, defaults={'password': make_password(password)})

        if created:
            clayful_customer_client = ClayfulCustomerClient()
            clayful_register = clayful_customer_client.clayful_register(email=email, nickname='용감한 거북이')

            if not clayful_register.status == 201:
                user.delete()
                raise ValidationError({'error_msg': '서버 에러입니다. 다시 시도해주세요.'})
            else:
                clayful_login = clayful_customer_client.clayful_login(email=email)
                token = clayful_login.data['token']
                user_id = clayful_login.data['customer']

            user_profile = Profile.objects.create(user=user, clayful_token=token, nickname='용감한 거북이')
            clayful_customer_client.clayful_customer_add_coupon(customer_id=user_id, coupon_id=settings.CLAYFUL_COUPON_ID)
            user_profile.save()

        refresh = RefreshToken.for_user(user)
        return {
            'access': refresh.access_token,
            'refresh': refresh,
        }


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['nickname', 'profile_image', 'points', 'firebase_token']


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
