from django.urls import path
from api.commerce.coupon.views import CouponUserListCreateView, CouponListView

urlpatterns = [
    path('list/', CouponListView.as_view()),
    path('user/', CouponUserListCreateView.as_view()),
]
