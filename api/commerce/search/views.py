from api.clayful_client import ClayfulProductClient, ClayfulBrandClient
from api.commerce.brand.serializers import BrandListRetrieveSerializer
from api.commerce.product.serializers import ProductListSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from api.commerce.list_helper import get_index
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
def search_list(request, *args, **kwargs):
    try:
        keyword = kwargs.get('keyword')
        page = kwargs.get('page', 1)
        if keyword.strip() == '':
            raise ValidationError({'error_msg': '검색어를 입력 해주세요.'})
        clf_product_client = ClayfulProductClient()
        clf_brand_client = ClayfulBrandClient()
        product_response = clf_product_client.search_products(keyword=keyword, page=page)
        brand_response = clf_brand_client.search_brands(keyword=keyword)
        if not brand_response.status == 200 and product_response.status == 200:
            raise ValidationError({'error_msg': '다시 한 번 시도 해주세요.'})
        product_count = clf_product_client.search_products_count(keyword=keyword).data['count']['raw']
        max_index, previous, next_val = get_index(request, product_count, page)
        if product_response.data:
            serialized_products = ProductListSerializer(product_response.data, many=True).data
        else:
            serialized_products = []
        if brand_response.data:
            serialized_brands = BrandListRetrieveSerializer(brand_response.data, many=True).data
        else:
            serialized_brands = []
        return Response(
            {'previous': previous, 'next': next_val, 'count': 10, 'results':
                {'products': serialized_products, 'brands': serialized_brands}}, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '다시 한 번 시도 해주세요.'})