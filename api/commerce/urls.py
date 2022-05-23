from django.urls import path, include

urlpatterns = [
    path('cart/', include('api.commerce.cart.urls')),
    path('order/', include('api.commerce.order.urls')),
    path('brand/', include('api.commerce.brand.urls')),
    path('review/', include('api.commerce.review.urls')),
    path('coupon/', include('api.commerce.coupon.urls')),
    path('product/', include('api.commerce.product.urls')),
    path('invoice/', include('api.commerce.invoice.urls')),
    path('address/', include('api.commerce.address.urls')),
    path('category/', include('api.commerce.category.urls')),
    path('checkout/', include('api.commerce.checkout.urls')),
]
