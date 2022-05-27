from rest_framework.generics import UpdateAPIView, CreateAPIView, ListAPIView, \
    RetrieveAPIView, DestroyAPIView, RetrieveUpdateAPIView
from api.notification.models import Notification
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from api.notification.serializers import NotificationSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Notification.objects.all()


class NotificationDetailView(RetrieveAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.hits += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_object(self):
        return Notification.objects.get(id=self.kwargs['id'])

# class NotificationReviewListView(ListAPIView):
#     serializer_class = Notification
#     pagination_class = StandardResultsSetPagination
#     permission_classes = [AllowAny]