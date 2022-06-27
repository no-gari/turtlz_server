from django.urls import path
from api.commerce.collection.views import get_big_collections, MainCollectionView, get_small_collections

urlpatterns = [
    path('', get_big_collections),
    path('main/list/', MainCollectionView.as_view()),
    path('<str:parent>/', get_small_collections),
    # path('banner/', BannerCollectionView.as_view()),
    # path('<str:parent>/banner/', get_banner_collection),
]
