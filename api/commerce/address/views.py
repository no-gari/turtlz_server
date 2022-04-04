from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView, CreateAPIView
from api.commerce.address.serializers import AddressSerializer
from rest_framework.permissions import IsAuthenticated
from api.commerce.address.models import Address


class CreateAddressView(CreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class AddressListView(ListAPIView):
    serializer_class = AddressSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.select_related('user').filter(user=self.request.user)


class AddressRetrieveDestroyView(RetrieveDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Address.objects.select_related('user').get(user=self.request.user, id=self.kwargs['pk'])
