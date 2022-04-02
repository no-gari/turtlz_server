from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from api.commerce.cart.serializers import CartSerializer, CartItemCreateSerializer
from rest_framework.permissions import IsAuthenticated
from api.commerce.cart.models import Cart


class CreateCartItemView(CreateAPIView):
    serializer_class = CartItemCreateSerializer
    permission_classes = [IsAuthenticated]


class CartRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.prefetch_related('cart_item_set').get_or_create(user=self.request.user)
        return cart
