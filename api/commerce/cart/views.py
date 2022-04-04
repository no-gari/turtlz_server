from api.commerce.cart.serializers import CartItemSerializer, CartItemCreateSerializer, CartProductSerializer
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from api.commerce.cart.models import CartItem


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


class CartItemListView(ListAPIView):
    serializer_class = CartProductSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.select_related('user').filter(user=self.request.user)
