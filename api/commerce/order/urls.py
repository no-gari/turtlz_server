from api.commerce.order.views import order_create, order_list, get_order, order_cancel, request_refund, order_done
from django.urls import path

urlpatterns = [
    path('list/', order_list),
    path('cancel-list/', order_list),
    path('create/', order_create),
    path('cancel/', order_cancel),
    path('<str:order_id>/', get_order),
    path('order-done/<str:order_id>/', order_done),
    path('request-refund/<str:order_id>/', request_refund),
]
