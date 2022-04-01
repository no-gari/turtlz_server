from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from api.commerce.cart.serializers import CartItemSerializer, CartSerializer
from rest_framework.permissions import IsAuthenticated
from api.commerce.cart.models import Cart


class CreateCartItemView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer


class CartRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    serializer_class = CartSerializer

    def get_object(self):
        cart, created = Cart.objects.prefetch_related('cart_item_set').get_or_create(user=self.request.user)
        return cart
