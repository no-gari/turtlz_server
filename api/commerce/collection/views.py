from api.commerce.collection.serializers import CollectionRetrieveSerializers, PopUpCollectionRetrieveSerializers
from api.clayful_client import ClayfulCollectionClient, ClayfulProductClient
from rest_framework.decorators import api_view, permission_classes
from api.commerce.product.serializers import ProductListSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import CollectionModel
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


@api_view(["GET"])
@permission_classes([AllowAny])
def get_banner_collections(request, *args, **kwargs):
    clayful_collection_client = ClayfulCollectionClient()
    try:
        response = clayful_collection_client.get_collections(parent=settings.CLAYFUL_CAMPING_ID)
        large_categories = CollectionRetrieveSerializers(response.data, many=True).data
        return Response(large_categories, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '카테고리를 가져오지 못했습니다.'})


@api_view(["GET"])
@permission_classes([AllowAny])
def get_main_collections(request, *args, **kwargs):
    clayful_collection_client = ClayfulCollectionClient()
    clayful_product_client = ClayfulProductClient()
    try:
        collections = clayful_collection_client.get_collections(parent=settings.CLAYFUL_COLLECTION_ID).data
        main_collections = []
        for collection in collections:
            product_response = clayful_product_client.list_products(collection=collection['_id'], page=1, sort='rating.count', brand='any').data
            product_serialized_data = ProductListSerializer(product_response, many=True).data
            main_collections.append({
                'collection': {
                    '_id': collection['_id'],
                    'name': collection['name'],
                    'thumbnail': ''
                }, 'products': product_serialized_data
            })
        return Response(main_collections, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '메인 콜렉션을 가져오지 못했습니다.'})


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


@api_view(["GET"])
@permission_classes([AllowAny])
def get_pop_up_collection(request, *args, **kwargs):
    try:
        collection = PopUpCollectionRetrieveSerializers(CollectionModel.objects.all(), many=True).data
        return Response(collection, status=status.HTTP_200_OK)
    except:
        raise ValidationError({'error_msg': '카테고리를 가져오지 못했습니다.'})
