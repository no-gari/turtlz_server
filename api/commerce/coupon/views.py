from api.commerce.coupon.serializers import CouponSerializer, CouponDetailSerializer
from api.clayful_client import ClayfulCouponClient, ClayfulCustomerClient
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


class CouponListView(ListAPIView):
    serializer_class = CouponSerializer

    def get_queryset(self):
        clf_coupon_client = ClayfulCouponClient()
        response = clf_coupon_client.coupon_list()
        if response.status != 200:
            raise ValidationError({'error_msg': '쿠폰 목록을 불러오는데 실패했습니다.'})
        return response.data


class CouponRetrieveView(RetrieveAPIView):
    serializer_class = CouponDetailSerializer
    lookup_field = 'coupon_id'

    def get_object(self, **kwargs):
        clf_coupon_client = ClayfulCouponClient()
        response = clf_coupon_client.coupon_detail(coupon_id=self.kwargs['coupon_id'])
        if response.status != 200:
            raise ValidationError({'error_msg': '쿠폰을 불러오는데 실패했습니다.'})
        return response.data


class MyCouponListView(ListAPIView):
    serializer_class = CouponSerializer

    def get_queryset(self):
        clf_customer_client = ClayfulCustomerClient()
        response = clf_customer_client.clayful_customer_coupons_list(clayful=self.request.user.profile.clayful_token)
        if response.status != 200:
            raise ValidationError({'error_msg': '쿠폰 목록을 불러오는데 실패했습니다.'})
        return response.data


@api_view(["GET"])
def coupon_count(request, *args, **kwargs):
    try:
        clf_coupon_client = ClayfulCouponClient()
        response = clf_coupon_client.coupon_count()
        if response.status == 200:
            return Response({'count': response.data['']}, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '상품 에러입니다.'})


@api_view(["POST"])
def coupon_issue(request, *args, **kwargs):
    try:
        clf_customer_client = ClayfulCustomerClient()
        customer_id = clf_customer_client.clayful_customer_get_me(clayful=request.user.profile.clayful_token)
        # 위에서 아이디 구해서 밑에다 넣어야 됨.
        response = clf_customer_client.clayful_customer_add_coupon(customer_id=customer_id, coupon_id=kwargs['coupon_id'])
        return response
    except:
        raise ValidationError({'error_msg': '쿠폰 발행에 실패했습니다.'})
