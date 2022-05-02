from django.urls import path
from api.commerce.order.views import OrderCreateView, OrderListView, OrderRetrieveView, GiftCreateView

urlpatterns = [
    # 일반적인 주문
    path('create/', OrderCreateView.as_view()),
    path('list/', OrderListView.as_view()),
    path('<str:order_number>/', OrderRetrieveView.as_view()),

    # 선물하기
    path('gift/create', GiftCreateView.as_view()),
    path('gift/<str:order_number>/'),
]
