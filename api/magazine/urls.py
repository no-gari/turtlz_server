from api.magazine.views import MagazinesListView, MagazineLikeUpdateView, MainMagazinesListView, \
    MainBannerMagazineListView, MagazineRetrieveView, ScrappedMagazinesListView, MagazineScrapUpdateView, \
    MagazineReviewsListView, MagazineReviewCreateView, MagazineCommentUpdateView, MagazineCommentDeleteView, \
    CatalogListView, CatalogDetailView
from django.urls import path

urlpatterns = [
    # 오늘의 매거진
    path('list/is-main/', MainMagazinesListView.as_view()),
    # 배너에 실리는 매거진
    path('list/is-main/banner/', MainBannerMagazineListView.as_view()),
    # 카탈로그 매거진
    path('list/catalog/', CatalogListView.as_view()),
    # 카탈로그 상세 뷰
    path('list/catalog/<int:id>/', CatalogDetailView.as_view()),
    path('list/', MagazinesListView.as_view()),
    path('detail/<int:id>/', MagazineRetrieveView.as_view()),
    path('list/scrapped/', ScrappedMagazinesListView.as_view()),
    path('detail/<int:id>/update-like/', MagazineLikeUpdateView.as_view()),
    path('detail/<int:id>/update-scrap/', MagazineScrapUpdateView.as_view()),
    path('detail/<int:id>/reviews/', MagazineReviewsListView.as_view()),
    path('detail/reviews/review-create/', MagazineReviewCreateView.as_view()),
    path('detail/<int:id>/review/update/', MagazineCommentUpdateView.as_view()),
    path('detail/<int:id>/review/delete/', MagazineCommentDeleteView.as_view()),
]
