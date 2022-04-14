from api.commerce.cart.serializers import CartItemSerializer, CartItemCreateSerializer, CartProductSerializer
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from api.commerce.cart.models import CartItem
from rest_framework.response import Response
from rest_framework import status
from json import loads, dumps


class CartItemRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = ['put', 'delete']

    def get_object(self):
        cart_item = CartItem.objects.select_related('user').get(user=self.request.user, product_variant=self.request.POST['product_variant'])
        return cart_item


class CartItemCreateView(CreateAPIView):
    serializer_class = CartItemCreateSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.select_related('user')


# 개 더럽게 짰음 ㅠ
class CartItemListView(ListAPIView):
    serializer_class = CartProductSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.select_related('user').filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()
        cart_products = loads(dumps(self.get_serializer(instance, many=True).data))
        product_list = self.new_list(cart_products)
        return Response(product_list, status=status.HTTP_200_OK)

    def new_list(self, datas):
        new_product_list = []
        for data in datas:
            index = next((index for (index, d) in enumerate(new_product_list) if d.get('id') == data['brand_id']), None)
            if index is None:
                new_product_list.append({
                    'id': data['brand_id'],
                    'name': data['brand_name'],
                    'least_price': data['brand_least_price'],
                    'shipping_price': data['brand_shipping_price'],
                    'products': [
                        {
                            'name': data['product']['name'],
                            'banner_img': data['product']['banner_img'],
                            'discount_price': data['product']['discount_price'],
                            'quantity': data['quantity'],
                            'variant_id': data['variant_id'],
                            'variant_name': data['variant_name'],
                        }
                    ]
                })
            else:
                new_product_list[index]['products'].append(
                    {
                        'name': data['product']['name'],
                        'banner_img': data['product']['banner_img'],
                        'discount_price': data['product']['discount_price'],
                        'quantity': data['quantity'],
                        'variant_id': data['variant_id'],
                        'variant_name': data['variant_name'],
                    }
                )
        return new_product_list
