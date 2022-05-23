from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.commerce.order.serializers import OrderItemSerializer, OrderItemCreateSerializer, OrderSerializer, OrderCreateSerializer
from api.commerce.order.models import Order, OrderItem
from api.utils import StandardResultsSetPagination


class OrderCreateView(CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]


class OrderRetrieveView(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'order_number'

    def get_object(self):
        return Order.objects.select_related('user').get(user=self.request.user, order_number=self.kwargs['order_number'])


class OrderListView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Order.objects.prefetch_related('user').filter(user=self.request.user)


class OrderDoneView(CreateAPIView):
    pass
