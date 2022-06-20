from api.commerce.order.serializers import QueryOptionSerializer, OrderSerializer, PaymentSerializer, MyOrderSerializer
from api.clayful_client import ClayfulOrderClient, ClayfulCartClient
from rest_framework.exceptions import ValidationError
from api.commerce.list_helper import get_index
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["POST"])
def order_create(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        clf_client = ClayfulCartClient(auth_token=request.user.profile.clayful_token)
        first = request.data['products'][0]
        if first['_id'] is None:
            products = ''
            for data in request.data['products']:
                add = clf_client.add_item(product_id=data['product_id'], variant=data['variant_id'],
                                          quantity=data['quantity'])
                products += add.data['_id']
                if not data == request.data['products'][-1]:
                    products += ','
            items = {'products': products}
        else:
            items = QueryOptionSerializer(request.data['products']).data
        payload = OrderSerializer(request.data).data
        response = clf_client.checkout_cart(items=items, payload=payload)
        if response.status == 201:
            return Response(PaymentSerializer(response.data['order']).data, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '주문에 실패했습니다.'})


@api_view(["POST"])
def order_cancel(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        clf_client = ClayfulOrderClient(auth_token=request.user.profile.clayful_token)
        order_id, payload = request.data['order_id'], {'reason': request.data.get('reason', '...')}
        response = clf_client.order_cancel(order_id=order_id, payload=payload)
        if response.status == 200:
            return Response(status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '주문 취소에 실패했습니다.'})


@api_view(["GET"])
def order_list(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        page = kwargs.get('page', 1)
        clf_order_client = ClayfulOrderClient(auth_token=request.user.profile.clayful_token)
        order_count = clf_order_client.order_count().data
        max_index, previous, next_val = get_index(request, order_count['count']['raw'], page)
        order = clf_order_client.get_order_list(page=page)
        serialized_data = MyOrderSerializer(order.data, many=True).data
        if order.status == 200:
            return Response(
                {'previous': previous, 'next': next_val, 'count': 10, 'results': serialized_data}, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '주문 내역을 불러올 수 없습니다.'})


@api_view(["GET"])
def cancel_list(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        page = kwargs.get('page', 1)
        clf_order_client = ClayfulOrderClient(auth_token=request.user.profile.clayful_token)
        order_count = clf_order_client.order_count().data
        max_index, previous, next_val = get_index(request, order_count['count']['raw'], page)
        order = clf_order_client.get_cancel_list(page=page)
        serialized_data = MyOrderSerializer(order.data, many=True).data
        if order.status == 200:
            return Response(
                {'previous': previous, 'next': next_val, 'count': 10, 'results': serialized_data}, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '주문 내역을 불러올 수 없습니다.'})


@api_view(["GET"])
def get_order(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        clf_order_client = ClayfulOrderClient(auth_token=request.user.profile.clayful_token)
        order = clf_order_client.get_order(order_id=kwargs['order_id'])
        if order.status == 200:
            serialized_data = MyOrderSerializer(order.data).data
            return Response(serialized_data, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '주문 내역을 불러올 수 없습니다.'})


@api_view(["POST"])
def order_done(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        clf_order_client = ClayfulOrderClient(auth_token=request.user.profile.clayful_token)
        order = clf_order_client.order_done(order_id=kwargs['order_id'])
        if order.status == 200:
            return Response(status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '주문 확정에 실패했습니다.'})


@api_view(["POST"])
def request_refund(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({'error_msg': '로그인 후 이용해주세요,'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        clf_order_client = ClayfulOrderClient(auth_token=request.user.profile.clayful_token)
        request_refund = clf_order_client.request_refund(order_id=kwargs['order_id'],
            reason=request.data['reason'], items=request.data['items'], quantity=request.data['quantity'])
        if request_refund.status == 200:
            return Response(status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '환불 요청에 실패했습니다.'})
