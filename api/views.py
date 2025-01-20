from pprint import pprint

from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from api.serializers import ListProductSerializer, DetailProductSerializer
from store.models import Product


@api_view(['GET'])
def list_products(request):
    products = Product.objects.all()
    serializer = ListProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def detail_product(request, id):
    product = get_object_or_404(Product, id=id)
    serializer = DetailProductSerializer(product,  context={'request': request})
    return Response(serializer.data)