from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from api.commerce.cart.serializers import CartItemSerializer
from rest_framework.permissions import IsAuthenticated
from api.commerce.cart.models import CartItem


class CartItemRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart_item = CartItem.objects.all()
        return cart_item


class CartItemListCreateView(ListCreateAPIView):
    serializer_class = CartItemSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all()
