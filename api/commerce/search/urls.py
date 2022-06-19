from api.commerce.search.views import search_list, SearchKeyword
from django.urls import path

urlpatterns = [
    path('<str:keyword>/', search_list),
    path('', SearchKeyword.as_view()),
]
