from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status


@api_view(["GET"])
def get_200(request, *args, **kwargs):
    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def ads(request):
    return HttpResponse("facebook.com, 571488096656037, RESELLER")
