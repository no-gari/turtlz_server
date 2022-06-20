from api.commerce.search.views import search_list, SearchKeyword, search_brand, search_product
from django.urls import path

urlpatterns = [
    path('<str:keyword>/', search_list),
    path('', SearchKeyword.as_view()),
    path('brand/<str:keyword>/', search_brand),
    path('product/<str:keyword>/', search_product),
]
