import hashlib

from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.iamport_client import IamportClient
from api.card.models import Card
from api.notice.models import Notice
from api.payment.models import Payment


class PaymentCreateSerializer(serializers.Serializer):
    membership_kind = serializers.CharField(write_only=True)
    card_kind = serializers.CharField(write_only=True)
    card_number = serializers.CharField(write_only=True)
    expiry = serializers.CharField(write_only=True)
    birth = serializers.CharField(write_only=True)
    pwd_2digit = serializers.CharField(write_only=True)
    is_change = serializers.BooleanField(write_only=True, required=False)

    def validate(self, attrs):
        self.user = self.context['request'].user

        if not attrs.get('is_change'):
            self.new_payment(attrs)
        else:
            self.change_payment(attrs)
        return attrs

    def new_payment(self, attrs):
        amount = 300
        created = timezone.now()
        card_4digit = attrs['card_number'][-4:]

        merchant_hash_string = str(created.timestamp()) + str(self.user.pk) + str(amount)
        customer_hash_string = str(created.timestamp()) + str(self.user.pk) + str(card_4digit)

        merchant_uid = hashlib.sha1(merchant_hash_string.encode('utf-8')).hexdigest()
        customer_uid = hashlib.sha1(customer_hash_string.encode('utf-8')).hexdigest()

        iamport_client = IamportClient()
        # 카드 등록 및 첫 결제
        try:
            card = Card.objects.create(
                user=self.user,
                customer_uid=customer_uid,
                last_4digits=card_4digit,
                kind=attrs['card_kind'],
                created=created,
            )
            payment = Payment(
                user=self.user,
                merchant_uid=merchant_uid,
                customer_uid=card.customer_uid,
                amount=amount,
                scheduled_at=created,
                created=created,
            )
            data = iamport_client.pay_onetime(
                merchant_uid=payment.merchant_uid,
                customer_uid=payment.customer_uid,
                amount=payment.amount,
                card_number=attrs['card_number'],
                expiry=f'20{attrs["expiry"][2:4]}{attrs["expiry"][0:2]}',
                pwd_2digit=attrs['pwd_2digit'],
                birth=attrs['birth'],
            )
            payment.status = data['status']
            payment.save()
        except (IamportClient.ResponseError, IamportClient.HttpError) as e:
            if '카드번호틀림' in e.message:
                error = {'card_number': '카드번호를 확인해주세요.'}
            elif '유효기간오류' in e.message:
                error = {'expiry': '유효기간을 확인해주세요.'}
            elif '비밀번호틀림' in e.message:
                error = {'pwd2digit': '비밀번호를 확인해주세요.'}
            elif '주민OR사업자등록번호오류' in e.message:
                error = {'birth': '생년월일 또는 사업자등록번호를 확인해주세요.'}
            elif '카드사 전화요망' in e.message:
                error = '카드사 전화요망'
            else:
                error = e.message
            raise ValidationError(error)

    def change_payment(self, attrs):
        amount = 100
        created = timezone.now()
        card_4digit = attrs['card_number'][-4:]

        merchant_hash_string = str(created.timestamp()) + str(self.user.pk) + str(amount)
        customer_hash_string = str(created.timestamp()) + str(self.user.pk) + str(card_4digit)

        merchant_uid = hashlib.sha1(merchant_hash_string.encode('utf-8')).hexdigest()
        customer_uid = hashlib.sha1(customer_hash_string.encode('utf-8')).hexdigest()

        iamport_client = IamportClient()
        # 카드 업데이트 및 100원 결제
        try:
            with transaction.atomic():
                card = self.user.card
                previous_customer_uid = card.customer_uid
                card.__dict__.update({
                    'customer_uid': customer_uid,
                    'last_4digits': card_4digit,
                    'kind': attrs['card_kind'],
                    'created': created,
                })
                card.save()
                previous_merchant_uid = merchant_uid
                data = iamport_client.pay_onetime(
                    merchant_uid=merchant_uid,
                    customer_uid=customer_uid,
                    amount=amount,
                    card_number=attrs['card_number'],
                    expiry=f'20{attrs["expiry"][2:4]}{attrs["expiry"][0:2]}',
                    pwd_2digit=attrs['pwd_2digit'],
                    birth=attrs['birth'],
                )
        except (IamportClient.ResponseError, IamportClient.HttpError) as e:
            if '카드번호틀림' in e.message:
                error = {'card_number': '카드번호를 확인해주세요.'}
            elif '유효기간오류' in e.message:
                error = {'expiry': '유효기간을 확인해주세요.'}
            elif '비밀번호틀림' in e.message:
                error = {'pwd2digit': '비밀번호를 확인해주세요.'}
            elif '주민OR사업자등록번호오류' in e.message:
                error = {'birth': '생년월일 또는 사업자등록번호를 확인해주세요.'}
            elif '카드사 전화요망' in e.message:
                error = '카드사 전화요망'
            else:
                error = e.message
            raise ValidationError(error)

        # 기존 스케줄링으로 새로운 스케줄링 및 기존 스케줄링 제거
        try:
            created = timezone.now()
            merchant_hash_string = str(created.timestamp()) + str(self.user.pk) + str(amount)
            merchant_uid = hashlib.sha1(merchant_hash_string.encode('utf-8')).hexdigest()

            last_payment = self.user.payment_set.first()
            payment = Payment(
                user=self.user,
                merchant_uid=merchant_uid,
                customer_uid=card.customer_uid,
                amount=last_payment.amount,
                scheduled_at=last_payment.scheduled_at,
                created=created,
            )
            data = iamport_client.pay_schedule(
                customer_uid=payment.customer_uid,
                schedules=[{
                    'merchant_uid': payment.merchant_uid,
                    'amount': payment.amount,
                    'schedule_at': int(last_payment.scheduled_at.timestamp()),
                }],
            )
            payment.status = data[0]['schedule_status']
            payment.save()

            iamport_client.pay_unschedule(customer_uid=previous_customer_uid)
            last_payment.delete()
        except (IamportClient.ResponseError, IamportClient.HttpError):
            raise ValidationError('스케줄링 및 기존 스케줄링 제거 실패')

        try:
            iamport_client.cancel_by_merchant_uid(merchant_uid=previous_merchant_uid, reason='카드 변경으로인한 결제')
        except (IamportClient.ResponseError, IamportClient.HttpError):
            raise ValidationError('100원 취소 실패')

    def create(self, validated_data):
        membership = self.user.membership
        if not validated_data.get('is_change'):
            membership.kind = validated_data['membership_kind']
            membership.save()
            Notice.objects.create(
                user=self.user,
                title='회원 등급이 업데이트 되었습니다.',
                body=f'회원 등급이 {membership.get_kind_display()}로 업데이트 되었습니다.'
            )

        return {'membership_kind': membership.kind}


class PaymentCallbackSerializer(serializers.Serializer):
    imp_uid = serializers.CharField(write_only=True)
    status = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if not attrs['status'] == 'paid':
            raise ValidationError('결제완료 콜백이 아닙니다.')
        iamport_client = IamportClient()
        try:
            data = iamport_client.find_by_imp_uid(attrs['imp_uid'])
        except (IamportClient.ResponseError, IamportClient.HttpError) as e:
            raise ValidationError('imp_uid를 iamport 서버에서 찾을 수 없습니다.')

        merchant_uid = data['merchant_uid']

        try:
            payment = attrs['payment'] = Payment.objects.get(merchant_uid=merchant_uid)
            payment.status = data['status']
            payment.save()
        except Payment.DoesNotExist:
            raise ValidationError('결제내역을 찾을 수 없습니다.')

        # 스케쥴 등록
        try:
            with transaction.atomic():
                user = payment.user
                created = timezone.now()

                merchant_hash_string = str(created.timestamp()) + str(user.pk) + str(payment.amount)
                merchant_uid = hashlib.sha1(merchant_hash_string.encode('utf-8')).hexdigest()
                scheduled_at = created + relativedelta(months=1)
                count = Payment.objects.filter(
                    scheduled_at__year=scheduled_at.year,
                    scheduled_at__month=scheduled_at.month,
                    scheduled_at__day=scheduled_at.day,
                ).count()
                scheduled_at = timezone.datetime(
                    scheduled_at.year,
                    scheduled_at.month,
                    scheduled_at.day,
                    9, 0, 0,
                ) + timezone.timedelta(minutes=count)
                new_payment = Payment(
                    user=user,
                    merchant_uid=merchant_uid,
                    customer_uid=user.card.customer_uid,
                    amount=payment.amount,
                    scheduled_at=scheduled_at,
                    created=created,
                )
                data = iamport_client.pay_schedule(
                    customer_uid=new_payment.customer_uid,
                    schedules=[{
                        'merchant_uid': new_payment.merchant_uid,
                        'amount': new_payment.amount,
                        'schedule_at': int(scheduled_at.timestamp()),
                    }],
                )
                new_payment.status = data[0]['schedule_status']
                new_payment.save()
        except (IamportClient.ResponseError, IamportClient.HttpError) as e:
            raise ValidationError('스케줄링 실패')

        return attrs

    def create(self, validated_data):
        return {}
