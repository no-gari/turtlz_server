from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from api.commerce.cart.models import Cart
from rest_framework.permissions import IsAuthenticated


class CreateCartItemView(CreateAPIView):
    permission_classes = [IsAuthenticated]


class CartRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        cart, created = Cart.objects.get(user=self.request.user)
        return cart
