from .serializers import BrandRetrieveSerializer, BrandListRetrieveSerializer, BrandDetailMagazineSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from api.clayful_client import ClayfulBrandClient
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from api.magazine.models import Magazines
from ..list_helper import get_index
from rest_framework import status


@api_view(["GET"])
@permission_classes([AllowAny])
def get_brand(request, *args, **kwargs):
    clayful_brand_client = ClayfulBrandClient()
    try:
        response = clayful_brand_client.get_brand(brand_id=kwargs['brand_id'])
        if not response.status == 200:
            raise ValidationError({'error_msg': '브랜드를 불러올 수 없습니다.'})
        serializer = BrandRetrieveSerializer(response.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception:
        raise ValidationError({'error_msg': '브랜드를 불러올 수 없습니다.'})


@api_view(["GET"])
@permission_classes([AllowAny])
def get_brand_product(request, *args, **kwargs):
    try:
        magazines = Magazines.objects.filter(brand=kwargs['brand_id'])
        serializer = BrandDetailMagazineSerializer(magazines)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception:
        raise ValidationError({'error_msg': '브랜드를 불러올 수 없습니다.'})


@api_view(["GET"])
@permission_classes([AllowAny])
def get_brand_list(request, *args, **kwargs):
    clayful_brand_client = ClayfulBrandClient()
    page = kwargs.get('page', 1)
    try:
        brand_client = clayful_brand_client.get_brand_count().data
        max_index, previous, next_val = get_index(request, brand_client['count']['raw'], page)
        brand_list = clayful_brand_client.get_brand_list(page=page)
        if not brand_list.status == 200:
            raise ValidationError({'error_msg': '브랜드 목록을 불러올 수 없습니다.'})
        serialized_data = BrandListRetrieveSerializer(brand_list.data, many=True).data
        return Response({'previous': previous, 'next': next_val, 'count': 10, 'results': serialized_data}, status=status.HTTP_200_OK)
    except Exception:
        raise ValidationError({'error_msg': '브랜드 목록을 불러올 수 없습니다.'})
