from api.commerce.address.views import CreateAddressView, AddressListView, AddressRetrieveDestroyView
from django.urls import path

urlpatterns = [
    path('', AddressRetrieveDestroyView.as_view()),
    path('add/', CreateAddressView.as_view()),
    path('list/', AddressListView.as_view()),
]
