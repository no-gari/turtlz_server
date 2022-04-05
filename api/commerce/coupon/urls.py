from django.urls import path
from api.commerce.coupon.views import CouponUserListView, CouponListView, CouponUserCreateView

urlpatterns = [
    path('list/', CouponListView.as_view()),
    path('user/', CouponUserListView.as_view()),
    path('user/create/', CouponUserCreateView.as_view()),
]
