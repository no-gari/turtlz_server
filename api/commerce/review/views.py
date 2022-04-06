from api.commerce.review.serializers import ReviewCreateSerializer, ReviewListSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView, ListAPIView
from api.commerce.review.models import Reviews


class ReviewCreateAPIView(CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated]


class ReviewListView(ListAPIView):
    serializer_class = ReviewListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Reviews.objects.select_related('order_item').filter(order_item__product_variant__product_id=self.request.POST['product_id'])
