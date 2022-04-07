from django.urls import path
from api.commerce.order.views import OrderCreateView, OrderListView, OrderRetrieveView

urlpatterns = [
    path('create/', OrderCreateView.as_view()),
    path('list/', OrderListView.as_view()),
    path('<str:order_number>/', OrderRetrieveView.as_view()),
]
