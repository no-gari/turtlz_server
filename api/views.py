from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
def get_200(request, *args, **kwargs):
    return Response(status=status.HTTP_200_OK)
