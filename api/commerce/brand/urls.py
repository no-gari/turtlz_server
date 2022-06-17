from django.urls import path
from api.commerce.brand.views import get_brand, get_brand_list, get_brand_product

urlpatterns = [
    path('<str:brand_id>/', get_brand),
    path('product-detail/<str:brand_id>/', get_brand_product),
    path('brands/list/', get_brand_list),
]
