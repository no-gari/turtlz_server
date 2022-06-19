from api.clayful_client import ClayfulReviewClient, ClayfulReviewCommentClient
from .serializers import ReviewCreateSerializer, ReviewDeleteSerializer, \
    ReviewRetrieveSerializer, ReviewListSerializer, ReviewCountSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
@permission_classes([AllowAny])
def reviews_count(request, *args, **kwargs):
    try:
        clayful_review_client = ClayfulReviewClient(auth_token=None)
        response = clayful_review_client.reviews_count(product=kwargs['product'])
        return Response(response.data, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '리뷰 개수를 불러오는데 실패했습니다.'})


@api_view(["GET"])
@permission_classes([AllowAny])
def reviews_list(request, *args, **kwargs):
    try:
        clayful_review_client = ClayfulReviewClient(auth_token=None)
        response = clayful_review_client.reviews_list(product=kwargs['product'], page=kwargs['page'])
        return Response(response.data, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '리뷰 리스트를 불러오는데 실패했습니다.'})


@api_view(["GET"])
@permission_classes([AllowAny])
def get_review(request, *args, **kwargs):
    try:
        clayful_review_client = ClayfulReviewClient(auth_token=None)
        response = clayful_review_client.get_review(review_id=kwargs['review_id'])
        return Response(response.data, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '리뷰를 불러오는데 실패했습니다.'})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_review(request, *args, **kwargs):
    try:
        clayful_review_client = ClayfulReviewClient(auth_token=request.META['HTTP_CLAYFUL'])
        response = clayful_review_client.create_review(
            customer=request.header['clayful'],
            order=request.data['order'],
            product=request.data['product'],
            body=request.data['body']
        )
        return Response(response.data, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '리뷰를 생성하는데 실패했습니다.'})


@api_view(["GET"])
@permission_classes([AllowAny])
def get_review_comment(request, *args, **kwargs):
    try:
        clayful_review_comment_client = ClayfulReviewCommentClient()
        response = clayful_review_comment_client.get_comments(review_id=kwargs['review_id'])
        return Response(response.data, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '리뷰를 불러오는데 실패했습니다.'})
