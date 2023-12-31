from api.commerce.review.views import reviews_list, reviews_count, get_review, create_review, get_review_comment
from django.urls import path

urlpatterns = [
    path('list/<str:product>/', reviews_list),
    path('count/<str:product>/', reviews_count),
    path('detail/<str:review_id>/', get_review),
    path('create/', create_review),

    path('review-comment/<str:review_id>/', get_review_comment)
    # path('delete/', delete_review),
]
