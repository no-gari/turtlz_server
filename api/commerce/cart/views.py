from rest_framework.generics import UpdateAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView
from api.commerce.cart.serializers import CartSerializer, CartItemCreateSerializer, CartItemSerializer
from rest_framework.permissions import IsAuthenticated
from api.commerce.cart.models import Cart, CartItem


class CreateCartItemView(CreateAPIView):
    serializer_class = CartItemCreateSerializer
    permission_classes = [IsAuthenticated]


class UpdateCartItemView(UpdateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all()
    allowed_methods = ['put']


class DestroyCartItemView(DestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all()


class CartRetrieveUpdateDestroyView(RetrieveAPIView):
    serializer_class = CartSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.prefetch_related('cart_item_set').get_or_create(user=self.request.user)
        return cart
