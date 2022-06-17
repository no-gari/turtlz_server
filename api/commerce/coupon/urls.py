from api.commerce.coupon.views import CouponListView, CouponRetrieveView, MyCouponListView, coupon_issue, coupon_count
from django.urls import path

urlpatterns = [
    path('detail/<str:coupon_id>/', CouponRetrieveView.as_view()),
    # path('my-coupon/list/', MyCouponListView.as_view()),
    path('list/', MyCouponListView.as_view()),
    path('count/', coupon_count),
    path('issue/', coupon_issue)
]
