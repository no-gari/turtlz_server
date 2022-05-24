from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.utils.translation import gettext_lazy as _
from api.utils import FilenameChanger
from django.db import models


class UserManager(DjangoUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.model.normalize_username(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    first_name = None
    last_name = None
    username = None
    email = models.EmailField(verbose_name=_('이메일'), unique=True)
    phone = models.CharField(verbose_name=_('휴대폰'), max_length=11, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    VERIFY_FIELDS = []
    REGISTER_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = '유저'
        verbose_name_plural = verbose_name
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    @property
    def is_social(self):
        return hasattr(self, 'social')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=32, verbose_name=_('닉네임'), null=True, blank=True)
    profile_image = models.ImageField(verbose_name=_('프로필 사진'), null=True, blank=True, upload_to=FilenameChanger('profile'))
    created_at = models.DateTimeField(verbose_name=_('생성 일자'), auto_now_add=True, null=True, blank=True)
    kind = models.CharField(max_length=32, verbose_name=_('종류'), null=True, blank=True)
    code = models.CharField(max_length=1024, verbose_name=_('SNS 고유 코드'), null=True, blank=True)
    points = models.PositiveIntegerField(default=0, verbose_name=_('포인트'))
    firebase_token = models.CharField(max_length=1024, verbose_name=_('파이어베이스 토큰'), null=True, blank=True)

    class Meta:
        verbose_name = '프로필'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.email + '의 프로필'


class SocialKindChoices(models.TextChoices):
    KAKAO = 'kakao', '카카오'
    APPLE = 'apple', '애플'


class EmailVerifier(models.Model):
    email = models.EmailField(verbose_name='이메일')
    code = models.CharField(verbose_name='인증번호', max_length=6)
    token = models.CharField(verbose_name='토큰', max_length=40)
    created = models.DateTimeField(verbose_name='생성일시')


class PhoneVerifier(models.Model):
    phone = models.CharField(verbose_name='휴대폰번호', max_length=11)
    code = models.CharField(verbose_name='인증번호', max_length=6)
    token = models.CharField(verbose_name='토큰', max_length=40)
    created = models.DateTimeField(verbose_name='생성일시')
