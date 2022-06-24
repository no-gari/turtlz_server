from api.commerce.collection.serializers import CollectionRetrieveSerializers
from api.clayful_client import ClayfulCollectionClient, ClayfulProductClient
from rest_framework.decorators import api_view, permission_classes
from api.commerce.product.serializers import ProductListSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings


@api_view(["GET"])
@permission_classes([AllowAny])
def get_big_collections(request, *args, **kwargs):
    clayful_collection_client = ClayfulCollectionClient()
    try:
        response = clayful_collection_client.get_collections(parent=settings.CLAYFUL_CAMPING_ID)
        large_categories = CollectionRetrieveSerializers(response.data, many=True).data
        return Response(large_categories, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '카테고리를 가져오지 못했습니다.'})


class MainCollectionView(ListAPIView):
    def get_queryset(self):
        try:
            brand = self.kwargs.get('brand', 'any')
            if self.kwargs.get('category') == '':
                category = settings.CLAYFUL_COLLECTION_ID
            else:
                category = self.kwargs.get('category', 'any')
            sort = self.request.query_params.get('sort', 'rating.count')
            page = self.request.query_params.get('page', '1')
            clayful_product_client = ClayfulProductClient()
            products = clayful_product_client.list_products(collection=category, page=page, sort=sort, brand=brand)
            if not products.status == 200:
                raise ValidationError({'error_msg': '서버 에러입니다. 잠시 후 다시 시도해주세요.'})
            return products.data
        except Exception:
            raise ValidationError({'error_msg': '상품을 불러올 수 없습니다.'})

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            brand = self.kwargs.get('brand', 'any')
            if self.kwargs.get('category') == '':
                category = settings.CLAYFUL_COLLECTION_ID
            else:
                category = self.kwargs.get('category', 'any')
            page = int(self.request.query_params.get('page', '1'))
            clf_product_client = ClayfulProductClient()
            serializer = ProductListSerializer(queryset, many=True)
            if not serializer.data == []:
                response = {'previous': str(int(page)-1), 'next':  str(int(page)+1), 'count': 10, 'results': serializer.data}
            else:
                response = {
                    'previous': None, 'next': None, 'count': None,
                    'result': {
                        '_id': None, 'name': None, 'hashtags': None, 'rating': None, 'original_price': None,
                        'discount_price': None, 'discount_rate': None, 'brand': None, 'thumbnail': None
                    }
                }
            return Response(response, status=status.HTTP_200_OK)
        except Exception:
            raise ValidationError({'error_msg': '상품을 불러올 수 없습니다.'})

@api_view(["GET"])
@permission_classes([AllowAny])
def get_small_collections(request, *args, **kwargs):
    clayful_collection_client = ClayfulCollectionClient()
    try:
        response = clayful_collection_client.get_collections(parent=settings.CLAYFUL_CAMPING_ID)
        large_categories = CollectionRetrieveSerializers(response.data, many=True).data
        serializer = CollectionRetrieveSerializers(large_categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '카테고리를 가져오지 못했습니다.'})
