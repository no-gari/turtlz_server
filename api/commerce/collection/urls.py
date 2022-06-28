from django.urls import path
from api.commerce.collection.views import get_big_collections, get_main_collections, get_small_collections, get_pop_up_collection

urlpatterns = [
    path('', get_big_collections),
    path('main/list/', get_main_collections),
    path('<str:parent>/', get_small_collections),
    path('collection/pop-up/', get_pop_up_collection),
    # path('banner/', BannerCollectionView.as_view()),
    # path('<str:parent>/banner/', get_banner_collection),
]
